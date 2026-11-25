from fastapi import HTTPException

def list_sessions(cx):
    return cx.execute("SELECT * FROM bench_sessions ORDER BY service_day DESC,open_minute,code").fetchall()

def session(cx, code):
    row=cx.execute("SELECT * FROM bench_sessions WHERE code=%s",(code,)).fetchone()
    if row is None:
        raise HTTPException(404,"使用单不存在")
    return row

def insert(cx, body):
    return cx.execute("""
        INSERT INTO bench_sessions(code,machine,crew,service_day,open_minute,end_minute)
        VALUES (%(code)s,%(machine)s,%(crew)s,%(service_day)s,%(open_minute)s,%(end_minute)s)
        RETURNING *
    """,body.model_dump()).fetchone()

def decide(cx, code, decision, reviewer):
    return cx.execute("""
        UPDATE bench_sessions SET decision=%s,checked_by=%s
        WHERE code=%s AND decision='logged' RETURNING *
    """,(decision,reviewer,code)).fetchone()
