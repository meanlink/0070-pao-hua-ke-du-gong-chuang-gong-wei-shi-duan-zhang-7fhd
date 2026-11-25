from datetime import date
from bench.report_store import bulletin

def aggregate(cx,payload):
    day=date.fromisoformat(payload["day"])
    items=bulletin(cx,day)["report"]
    occupied=sum(item["used"] for item in items)
    supply=sum(item["available"] for item in items)
    return {"day":str(day),"available":supply,"occupied":occupied,
            "weighted_pct":round(100*occupied/supply,2) if supply else None}
