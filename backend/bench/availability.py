from bench.intervals import clipped,subtract

def interval(record):
    return record["open_minute"],record["end_minute"]

def maintenance_for(cx, machine, day):
    return cx.execute("""
        SELECT * FROM maintenance_blocks WHERE machine=%s AND service_day=%s ORDER BY open_minute,code
    """,(machine,day)).fetchall()

def service_intervals(hours, maintenance):
    lo,hi=hours["lo"],hours["hi"]
    return subtract([(lo,hi)],clipped([interval(row) for row in maintenance],lo,hi))

def eligible_session(record, hours, maintenance):
    lo,hi=interval(record)
    return any(lo<b and hi>a for a,b in service_intervals(hours,maintenance))
