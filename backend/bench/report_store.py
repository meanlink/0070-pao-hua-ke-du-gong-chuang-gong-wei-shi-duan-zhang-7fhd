from psycopg.types.json import Jsonb

def calendar(cx,day):
    return cx.execute("""
        SELECT h.*,m.title,m.bay FROM shop_hours h JOIN machines m ON m.key=h.machine
        WHERE h.service_day=%s ORDER BY m.bay,m.key
    """,(day,)).fetchall()

def daily_sessions(cx,machine,day):
    return cx.execute("SELECT * FROM bench_sessions WHERE machine=%s AND service_day=%s",(machine,day)).fetchall()

def bulletin(cx,day):
    return cx.execute("SELECT * FROM utilization_bulletins WHERE service_day=%s",(day,)).fetchone()

def record(cx, day, email, report, job):
    return cx.execute("""
        INSERT INTO utilization_bulletins(service_day,issued_by,report,job_id)
        VALUES (%s,%s,%s,%s) RETURNING *
    """,(day,email,Jsonb(report),job)).fetchone()
