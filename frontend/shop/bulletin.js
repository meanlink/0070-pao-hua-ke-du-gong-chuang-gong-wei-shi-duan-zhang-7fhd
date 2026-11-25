import {api,h,empty} from '/base.js'
import {header} from './heading.js'
import {connect} from './forms.js'
import {rateLine} from './rate-line.js'

export async function bulletin(root,user,day) {
  const assets=await api('/api/bench/machines')
  day=day||assets[0]?.service_day
  if(!day) {root.innerHTML=empty('工位日历为空。');return}
  const report=await api('/api/bench/utilization/'+day)
  const job=report.job?await api('/api/jobs/'+report.job):null
  root.innerHTML=header('占用率公报','计入确认工单与有效开放区间的交集。同一设备相交的开机段合并后再计算。')
    +`<div class="shop-floor"><section><div class="rate-key"><span>开放</span><span>占用</span><small>时间轴 08:00—16:00</small></div>
    <ul class="rates">${report.rows.map(rateLine).join('')}</ul></section><aside><h2>${report.published?'已发布':'待签公报'}</h2>
    <label>班表日期<input type="date" value="${h(day)}"></label>
    ${report.published?`<p>汇总占用率 ${job?.status==='done'?(job.result.weighted_pct??'—')+'%':'待后台汇总'}</p>`:''}
    ${!report.published&&user.role==='reviewer'?`<form><button>签署公报</button><p role="status"></p></form>`:''}</aside></div>`
  root.querySelector('input').onchange=event=>{
    if(event.target.value) bulletin(root,user,event.target.value).catch(error=>root.innerHTML=empty(error.message))
  }
  connect(root.querySelector('form'),()=>api('/api/bench/utilization/'+day+'/publish','POST',{}),()=>bulletin(root,user,day))
}
