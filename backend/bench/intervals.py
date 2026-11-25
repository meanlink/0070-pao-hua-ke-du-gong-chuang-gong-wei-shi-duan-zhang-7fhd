def coalesce(intervals):
    union=[]
    for lo, hi in sorted(intervals):
        if lo >= hi:
            continue
        if union and union[-1][1] >= lo:
            union[-1] = (union[-1][0],max(hi, union[-1][1]))
        else:
            union.append((lo,hi))
    return union

def clipped(ranges, lo, hi):
    return coalesce((max(start,lo),min(end,hi)) for start,end in ranges)

def duration(intervals):
    return sum(hi-lo for lo,hi in intervals)

def subtract(ranges, exclusions):
    for start,end in exclusions:
        remaining=[]
        for lo,hi in ranges:
            if hi <= start or lo >= end:
                remaining.append((lo,hi))
            else:
                remaining.extend((a,b) for a,b in ((lo,start),(end,hi)) if a<b)
        ranges=remaining
    return ranges
