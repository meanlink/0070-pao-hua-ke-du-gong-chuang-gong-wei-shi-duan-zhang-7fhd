from fastapi import APIRouter,Depends
from core import db,require

router=APIRouter(prefix="/api/bench")

@router.get("/machines")
def machines(_=Depends(require())):
    with db() as cx:
        return cx.execute("""
            SELECT m.*,h.service_day,h.lo,h.hi
            FROM machines m JOIN shop_hours h ON h.machine=m.key ORDER BY h.service_day,m.bay,m.key
        """).fetchall()
