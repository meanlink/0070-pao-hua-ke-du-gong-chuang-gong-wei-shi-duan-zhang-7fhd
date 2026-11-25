import {api,h,empty} from '/base.js'
import {header} from './heading.js'
import {connect} from './forms.js'
import {rateLine} from './rate-line.js'

const minutes=value=>`<b>${h(value.used)} / ${h(value.available)}</b>`
const percent=value=>value.weighted_pct===null?'—':h(value.weighted_pct)+'%'

function correction(report,day) {
  if(!report.corrections?.length) return `<p class="muted">此日暂无移单更正。</p>`
  return `<ul class="corrections">${report.corrections.map(item=>`<li>
    <p><b>${h(item.session_code)}</b> 由 ${h(item.from_day)} 移至 ${h(item.to_day)}
      <small>移单凭据 ${h(item.request_key)} · ${h(item.moved_by)}</small></p>
    ${item.receipt.days.map(part=>`<div class="correction-day ${part.day===day?'is-current':''}">
      <strong>${h(part.day)}${part.role==='from'?'（移出日）':'（移入日）'}</strong>
      <span>更正前 ${minutes(part.before)} 分钟 · 总占用率 ${percent(part.before)}</span>
      <span>更正后 ${minutes(part.after)} 分钟 · 总占用率 ${percent(part.after)}</span>
    </div>`).join('')}</li>`).join('')}</ul>`
}

export async function bulletin(root,user,day) {
  const assets=await api('/api/bench/machines')
  day=day||assets[0]?.service_day
  if(!day) {root.innerHTML=empty('工位日历为空。');return}
  const report=await api('/api/bench/utilization/'+day)
  const job=report.job?await api('/api/jobs/'+report.job):null
  const total=job?.status==='done'?job.result.weighted_pct:report.totals.weighted_pct
  root.innerHTML=header('占用率公报','计入确认工单与有效开放区间的交集。同一设备相交的开机段合并后再计算。')
    +`<div class="shop-floor"><section><div class="rate-key"><span>开放</span><span>占用</span><small>时间轴 08:00—16:00</small></div>
    <ul class="rates">${report.rows.map(rateLine).join('')}</ul>
    <h2>移单更正对照</h2>${correction(report,day)}</section><aside><h2>${report.published?'已发布':'待签公报'}</h2>
    <label>班表日期<input type="date" value="${h(day)}"></label>
    ${report.published?`<p>汇总占用率 ${total===null||total===undefined?'—':h(total)+'%'}（${h(report.totals.used)} / ${h(report.totals.available)} 分钟）</p>`:''}
    ${!report.published&&user.role==='reviewer'?`<form><button>签署公报</button><p role="status"></p></form>`:''}</aside></div>`
  root.querySelector('input').onchange=event=>{
    if(event.target.value) bulletin(root,user,event.target.value).catch(error=>root.innerHTML=empty(error.message))
  }
  connect(root.querySelector('form'),()=>api('/api/bench/utilization/'+day+'/publish','POST',{}),()=>bulletin(root,user,day))
}
