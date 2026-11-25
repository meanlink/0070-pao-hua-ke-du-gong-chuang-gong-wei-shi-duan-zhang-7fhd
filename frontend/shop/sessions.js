import {api} from '/base.js'
import {header} from './heading.js'
import {fields} from './inputs.js'
import {connect} from './forms.js'
import {sessionRows} from './session-rows.js'

export async function records(root,user) {
  const [rows,assets]=await Promise.all([api('/api/bench/sessions'),api('/api/bench/machines')])
  const days=[...new Set(assets.map(row=>row.service_day))].sort()
  root.innerHTML=header('使用单复核','逐班核验实际使用时间。完全处在停机窗里的使用单只能冲销。纸单记错日期时，复核员可把已确认的使用单移到正确日期。')
    +`<div class="shop-floor"><div class="scroll"><table><thead><tr><th>使用单</th><th>设备</th><th>团队</th>
    <th>实际时段</th><th>审核</th></tr></thead><tbody>${sessionRows(rows,user.role==='reviewer')}</tbody></table></div>
    <aside><h2>开机流水</h2><p>提交实际发生的时间与使用班组。</p>${user.role==='operator'?`<form id="session-add">
    ${fields(assets)}<label>班组<input name="crew" minlength="2" maxlength="60" required></label><button>登记使用单</button>
    <p role="status"></p></form>`:''}
    ${user.role==='reviewer'?`<form id="session-move"><h3>移单更正</h3>
    <label>使用单<select name="code">${rows.filter(row=>row.decision==='counted').map(row=>`<option value="${row.code}">${row.code} · ${row.service_day}</option>`).join('')}</select></label>
    <label>移到日期<select name="to_day">${days.map(day=>`<option value="${day}">${day}</option>`).join('')}</select></label>
    <button>移到正确日期并重发两日公报</button><p role="status"></p></form>`:''}</aside></div>`
  const refresh=()=>records(root,user)
  connect(root.querySelector('#session-add'),data=>api('/api/bench/sessions','POST',data),refresh,true)
  const moveForm=root.querySelector('#session-move')
  // Keep one key per pending submission so a retry after a timeout is idempotent;
  // a confirmed success clears it so a later deliberate move gets a fresh key.
  let moveKey=moveForm?crypto.randomUUID():null
  if(moveForm) moveForm.oninput=()=>{moveKey=crypto.randomUUID()}
  connect(moveForm,data=>api('/api/bench/sessions/'+data.code+'/move','POST',
    {to_day:data.to_day,request_key:moveKey}),async()=>{
      moveKey=crypto.randomUUID()
      const moved=moveForm.querySelector('[role=status]')
      if(moved) moved.textContent='两日公报已按更正重算并切换。'
      await refresh()
    })
  for(const form of root.querySelectorAll('[data-session]'))
    connect(form,(_,button)=>api('/api/bench/sessions/'+form.dataset.session,'PUT',{decision:button.value}),refresh)
}
