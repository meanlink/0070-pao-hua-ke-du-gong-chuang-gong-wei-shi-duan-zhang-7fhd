"""Shared recomputation for a whole service day.

Both the ordinary bulletin reader and the correction path use these helpers so
that a moved slip and a freshly opened day agree on open windows, maintenance
and merged overlapping slips.
"""
from bench.availability import maintenance_for
from bench.report_store import calendar, daily_sessions
from bench.utilization import rate


def rows_for(cx, day):
    return [rate(hours, maintenance_for(cx, hours["machine"], day),
                 daily_sessions(cx, hours["machine"], day))
            for hours in calendar(cx, day)]


def totals(rows):
    used = sum(item["used"] for item in rows)
    available = sum(item["available"] for item in rows)
    return {
        "used": used,
        "available": available,
        "maintenance": sum(item["maintenance"] for item in rows),
        "weighted_pct": round(100 * used / available, 2) if available else None,
    }
