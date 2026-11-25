from bench.availability import interval,service_intervals
from bench.intervals import clipped,coalesce,duration

def rate(shift, blocks, sessions):
    windows=service_intervals(shift,blocks)
    raw=[interval(row) for row in sessions if row["decision"]=="counted"]
    counted=coalesce(part for lo,hi in windows for part in clipped(raw,lo,hi))
    available=duration(windows)
    used=duration(counted)
    return {
        "machine":shift["machine"], "title":shift["title"],"bay":shift["bay"],
        "planned":shift["hi"]-shift["lo"],"available":available,"used":used,
        "maintenance":shift["hi"]-shift["lo"]-available,
        "pending":sum(row["decision"]=="logged" for row in sessions),
        "pct":round(100*used/available,2) if available else None,
        "available_windows":windows,"occupied_windows":counted
    }
