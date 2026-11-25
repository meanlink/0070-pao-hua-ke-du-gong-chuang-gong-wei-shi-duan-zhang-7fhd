from fastapi import APIRouter,Depends
from core import db,require
from bench.models import Decide,Session
from bench.session_rules import log_session,review
from bench.session_store import list_sessions

router=APIRouter(prefix="/api/bench/sessions")

@router.get("")
def all_sessions(_=Depends(require())):
    with db() as cx:
        return list_sessions(cx)

@router.post("",status_code=201)
def add(body:Session,_=Depends(require("operator"))):
    with db() as cx:
        return log_session(cx,body)

@router.put("/{code}")
def settle(code:str,body:Decide,user=Depends(require("reviewer"))):
    with db() as cx:
        return review(cx,code,body,user["email"])
