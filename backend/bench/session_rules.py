from fastapi import HTTPException
from bench.availability import eligible_session,maintenance_for
from bench.days import editable,hours
from bench.session_store import decide,insert,session

def log_session(cx, body):
    editable(cx,body.service_day)
    hours(cx,body.machine,body.service_day)
    return insert(cx,body)

def review(cx, code, body, email):
    row=session(cx,code)
    editable(cx,row["service_day"])
    shift=hours(cx,row["machine"],row["service_day"])
    blocks=maintenance_for(cx,row["machine"],row["service_day"])
    if body.decision=="counted" and not eligible_session(row,shift,blocks):
        raise HTTPException(409,"流水全部落在停机或非开放时段，只能冲销")
    updated=decide(cx,code,body.decision,email)
    if not updated:
        raise HTTPException(409,"使用单已复核")
    return updated
