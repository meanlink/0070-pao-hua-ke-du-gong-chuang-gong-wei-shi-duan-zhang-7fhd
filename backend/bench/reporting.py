from fastapi import HTTPException
from core import enqueue
from bench import move_store
from bench.calc import rows_for, totals
from bench.days import editable,hold
from bench.report_store import bulletin,record

def report(cx,day):
    hold(cx,day)
    existing=bulletin(cx,day)
    if existing:
        rows=existing["report"]
        return {"rows":rows,"published":True,"job":existing["job_id"],
                "totals":totals(rows),"corrections":move_store.corrections(cx,day)}
    rows=rows_for(cx,day)
    return {"rows":rows,"published":False,"totals":totals(rows),
            "corrections":move_store.corrections(cx,day)}

def publish(cx, day, email):
    editable(cx,day)
    result=report(cx,day)
    if not result["rows"]:
        raise HTTPException(404,"当天没有排班开放记录")
    if any(item["pending"] for item in result["rows"]):
        raise HTTPException(409,"仍有未冲销或确认的使用单")
    job=enqueue(cx,"bench-bulletin",{"day":day.isoformat()})
    return record(cx,day,email,result["rows"],job)
