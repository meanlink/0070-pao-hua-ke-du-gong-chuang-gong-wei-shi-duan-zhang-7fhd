from fastapi import HTTPException

def hold(cx, day):
    cx.execute("SELECT pg_advisory_xact_lock(1940,%s)",(day.toordinal(),))

def editable(cx, day):
    hold(cx,day)
    if cx.execute("SELECT 1 FROM utilization_bulletins WHERE service_day=%s",(day,)).fetchone():
        raise HTTPException(409,"此日工位公报已发布")

def hours(cx, machine, day):
    row=cx.execute("SELECT * FROM shop_hours WHERE machine=%s AND service_day=%s",(machine,day)).fetchone()
    if not row:
        raise HTTPException(409,"设备当天未安排对外开放")
    return row
