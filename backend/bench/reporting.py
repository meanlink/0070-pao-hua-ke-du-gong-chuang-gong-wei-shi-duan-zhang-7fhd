from fastapi import HTTPException
from core import enqueue
from bench.availability import maintenance_for
from bench.days import editable,hold
from bench.report_store import bulletin,calendar,daily_sessions,record
from bench.utilization import rate

def report(cx,day):
    hold(cx,day)
    existing=bulletin(cx,day)
    if existing:
        return {"rows":existing["report"],"published":True,"job":existing["job_id"]}
    rows=[rate(hours,maintenance_for(cx,hours["machine"],day),daily_sessions(cx,hours["machine"],day))
          for hours in calendar(cx,day)]
    return {"rows":rows,"published":False}

def publish(cx, day, email):
    editable(cx,day)
    result=report(cx,day)
    if not result["rows"]:
        raise HTTPException(404,"当天没有排班开放记录")
    if any(item["pending"] for item in result["rows"]):
        raise HTTPException(409,"仍有未冲销或确认的使用单")
    job=enqueue(cx,"bench-bulletin",{"day":day.isoformat()})
    return record(cx,day,email,result["rows"],job)
