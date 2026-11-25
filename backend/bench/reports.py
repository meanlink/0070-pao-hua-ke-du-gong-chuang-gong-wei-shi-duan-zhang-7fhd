from datetime import date
from fastapi import APIRouter,Depends
from core import db,require
from bench.reporting import publish,report

router=APIRouter(prefix="/api/bench/utilization")

@router.get("/{day}")
def get_rates(day:date,_=Depends(require())):
    with db() as cx: return report(cx,day)

@router.post("/{day}/publish",status_code=201)
def issue(day:date,user=Depends(require("reviewer"))):
    with db() as cx: return publish(cx,day,user["email"])
