import {api} from '/base.js'
import {header} from './heading.js'
import {fields} from './inputs.js'
import {connect} from './forms.js'
import {sessionRows} from './session-rows.js'

export async function records(root,user) {
  const [rows,assets]=await Promise.all([api('/api/bench/sessions'),api('/api/bench/machines')])
  root.innerHTML=header('使用单复核','逐班核验实际使用时间。完全处在停机窗里的使用单只能冲销。')
    +`<div class="shop-floor"><div class="scroll"><table><thead><tr><th>使用单</th><th>设备</th><th>团队</th>
    <th>实际时段</th><th>审核</th></tr></thead><tbody>${sessionRows(rows,user.role==='reviewer')}</tbody></table></div>
    <aside><h2>开机流水</h2><p>提交实际发生的时间与使用班组。</p>${user.role==='operator'?`<form id="session-add">
    ${fields(assets)}<label>班组<input name="crew" minlength="2" maxlength="60" required></label><button>登记使用单</button>
    <p role="status"></p></form>`:''}</aside></div>`
  const refresh=()=>records(root,user)
  connect(root.querySelector('#session-add'),data=>api('/api/bench/sessions','POST',data),refresh,true)
  for(const form of root.querySelectorAll('[data-session]'))
    connect(form,(_,button)=>api('/api/bench/sessions/'+form.dataset.session,'PUT',{decision:button.value}),refresh)
}
