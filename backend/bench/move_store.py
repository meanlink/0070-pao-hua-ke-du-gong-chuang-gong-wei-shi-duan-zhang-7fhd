from psycopg.types.json import Jsonb


def by_key(cx, request_key):
    return cx.execute(
        "SELECT * FROM bench_session_moves WHERE request_key=%s", (request_key,)
    ).fetchone()


def record(cx, request_key, code, from_day, to_day, email, receipt):
    return cx.execute("""
        INSERT INTO bench_session_moves(request_key,session_code,from_day,to_day,moved_by,receipt)
        VALUES (%s,%s,%s,%s,%s,%s) RETURNING id,created_at
    """, (request_key, code, from_day, to_day, email, Jsonb(receipt))).fetchone()


def store_receipt(cx, move_id, receipt):
    return cx.execute(
        "UPDATE bench_session_moves SET receipt=%s WHERE id=%s RETURNING *",
        (Jsonb(receipt), move_id),
    ).fetchone()


def corrections(cx, day):
    return cx.execute("""
        SELECT id,request_key,session_code,from_day,to_day,moved_by,receipt,created_at
        FROM bench_session_moves
        WHERE from_day=%s OR to_day=%s
        ORDER BY created_at DESC,id DESC
    """, (day, day)).fetchall()
