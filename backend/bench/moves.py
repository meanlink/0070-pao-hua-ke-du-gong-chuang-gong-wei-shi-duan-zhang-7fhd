from datetime import date
from fastapi import APIRouter,Depends
from pydantic import BaseModel,Field
from core import db,require
from bench.move_rules import move

router=APIRouter(prefix="/api/bench/sessions")

class MoveRequest(BaseModel):
    to_day: date
    request_key: str = Field(min_length=8,max_length=100,pattern=r"^[A-Za-z0-9._:-]+$")

@router.post("/{code}/move")
def relocate(code:str,body:MoveRequest,user=Depends(require("reviewer"))):
    with db() as cx:
        return move(cx,code,body.to_day,body.request_key,user["email"])
