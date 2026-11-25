export const time=minute=>[Math.floor(minute/60),minute%60].map(n=>String(n).padStart(2,'0')).join(':')
export const hours=(lo,hi)=>time(lo)+'—'+time(hi)
export function minute(hhmm) {
  const [hour,min]=hhmm.split(':').map(Number)
  return 60*hour+min
}

export const labels={logged:'待核验',counted:'已确认',void:'已冲销'}
