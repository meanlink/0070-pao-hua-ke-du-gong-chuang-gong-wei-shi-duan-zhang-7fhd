from fastapi import APIRouter,Depends,HTTPException
from core import db,require
from bench.availability import eligible_session,maintenance_for
from bench.days import editable,hours
from bench.maintenance_store import insert_block,maintenance
from bench.models import Block

router=APIRouter(prefix="/api/bench/maintenance")

@router.get("")
def all_blocks(_=Depends(require())):
    with db() as cx:
        return maintenance(cx)

@router.post("",status_code=201)
def add_block(body:Block,_=Depends(require("operator"))):
    with db() as cx:
        editable(cx,body.service_day)
        opens=hours(cx,body.machine,body.service_day)
        prior=maintenance_for(cx,body.machine,body.service_day)
        active=cx.execute("""
            SELECT * FROM bench_sessions WHERE machine=%s AND service_day=%s AND decision='counted'
        """,(body.machine,body.service_day)).fetchall()
        if any(not eligible_session(row,opens,prior+[body.model_dump()]) for row in active):
            raise HTTPException(409,"新增维护将覆盖已确认的完整使用段，需先核对来源")
        return insert_block(cx,body)
