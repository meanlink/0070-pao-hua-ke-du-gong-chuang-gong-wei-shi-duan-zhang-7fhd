from datetime import date
from bench.calc import totals
from bench.report_store import bulletin

def aggregate(cx,payload):
    day=date.fromisoformat(payload["day"])
    row=bulletin(cx,day)
    if not row:
        raise ValueError(f"No issued bulletin for {day}")
    summary=totals(row["report"])
    return {"day":str(day),"available":summary["available"],
            "occupied":summary["used"],"weighted_pct":summary["weighted_pct"]}
