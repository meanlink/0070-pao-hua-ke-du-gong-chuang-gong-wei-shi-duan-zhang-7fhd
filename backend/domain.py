from fastapi import APIRouter
from bench import machines,maintenance,reports,sessions,moves
from bench.demo import seed
from bench.dispatch import aggregate

router=APIRouter()
for module in (machines,sessions,moves,maintenance,reports):
    router.include_router(module.router)

def run_job(cx,kind,payload):
    if kind=="bench-bulletin":
        return aggregate(cx,payload)
    raise ValueError(f"Unknown workshop task {kind}")
