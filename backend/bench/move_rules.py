"""Move a confirmed bench session to another working day.

Both affected bulletins are recomputed from open hours, maintenance blocks and
merged overlapping sessions, then replace the issued versions in a single
database transaction. A failed or rejected move leaves both days on their old
bulletins.

Locks: the session code is serialised first so a retried request key can be
recognised, then the two service days are locked in ordinal order (the same key
space used by maintenance and session edits). Concurrent moves that share a day
therefore queue up on that day and each recomputes after the previous commit, so
both are counted instead of overwriting each other.
"""
from datetime import datetime, timezone

from fastapi import HTTPException

from core import enqueue
from bench import move_store
from bench.availability import eligible_session, maintenance_for
from bench.calc import rows_for, totals
from bench.days import hours
from bench.report_store import bulletin, replace
from bench.session_store import session, session_for_update


def _hold_session(cx, code):
    cx.execute("SELECT pg_advisory_xact_lock(1941,hashtext(%s))", (code,))


def _hold_days(cx, days):
    for day in sorted(set(days)):
        cx.execute("SELECT pg_advisory_xact_lock(1940,%s)", (day.toordinal(),))


def _before(cx, day):
    issued = bulletin(cx, day)
    if not issued:
        raise HTTPException(409, "两日工位公报尚未全部签发，无法按更正切换")
    return totals(issued["report"])


def move(cx, code, to_day, request_key, email):
    # Serialise moves of the same slip and recognise a retried key before any
    # row lock is taken.
    _hold_session(cx, code)
    peek = session(cx, code)
    prior = move_store.by_key(cx, request_key)
    if prior:
        if prior["session_code"] != code or prior["to_day"] != to_day:
            raise HTTPException(409, "该移单凭据已用于另一笔更正")
        return {"receipt": prior["receipt"], "replayed": True}

    if peek["decision"] != "counted":
        raise HTTPException(409, "只有已确认的使用单可以移单")
    from_day = peek["service_day"]
    if to_day == from_day:
        raise HTTPException(409, "目标日期与当前日期相同")

    # Take the day locks before any row lock. Service edits and publishing lock
    # a day first and then the row, so locking the row earlier could deadlock.
    _hold_days(cx, [from_day, to_day])

    # Re-read with a row lock after the day locks: another correction may have
    # changed the slip in the meantime.
    row = session_for_update(cx, code)
    if row["service_day"] != from_day:
        raise HTTPException(409, "使用单日期已被其他更正调整，请刷新后重试")
    if row["decision"] != "counted":
        raise HTTPException(409, "使用单状态已变更，请刷新后重试")

    shift = hours(cx, row["machine"], to_day)
    blocks = maintenance_for(cx, row["machine"], to_day)
    if not eligible_session(row, shift, blocks):
        raise HTTPException(409, "目标日期该时段整段不可用，已退回原日期")

    before = {from_day: _before(cx, from_day), to_day: _before(cx, to_day)}

    cx.execute(
        "UPDATE bench_sessions SET service_day=%s WHERE code=%s", (to_day, code)
    )

    after_rows = {day: rows_for(cx, day) for day in (from_day, to_day)}
    after = {day: totals(after_rows[day]) for day in (from_day, to_day)}

    jobs = {}
    for day in (from_day, to_day):
        jobs[day] = enqueue(cx, "bench-bulletin", {"day": day.isoformat()})
        replace(cx, day, email, after_rows[day], jobs[day])

    receipt = {
        "request_key": request_key,
        "session": code,
        "machine": row["machine"],
        "crew": row["crew"],
        "span_minutes": row["end_minute"] - row["open_minute"],
        "from_day": from_day.isoformat(),
        "to_day": to_day.isoformat(),
        "moved_by": email,
        "days": [
            {
                "day": day.isoformat(),
                "role": role,
                "before": before[day],
                "after": after[day],
                "bulletin_job": jobs[day],
            }
            for day, role in ((from_day, "from"), (to_day, "to"))
        ],
    }
    saved = move_store.record(cx, request_key, code, from_day, to_day, email, receipt)
    receipt["move_id"] = saved["id"]
    receipt["created_at"] = saved["created_at"].isoformat()
    move_store.store_receipt(cx, saved["id"], receipt)
    return {"receipt": receipt, "replayed": False}
