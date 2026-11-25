import {api,h} from '/base.js'
import {header} from './heading.js'
import {fields} from './inputs.js'
import {connect} from './forms.js'
import {hours} from './time.js'
import {track} from './track.js'

export async function blocks(root,user) {
  const [rows,assets]=await Promise.all([api('/api/bench/maintenance'),api('/api/bench/machines')])
  root.innerHTML=header('维护禁用窗','停机班登记实际关停时间。同一设备连续或交叠的停机窗合并扣除。')
    +`<div class="shop-floor"><section class="block-book">${rows.map(row=>`<article>
       <span class="plate">${h(row.machine)}</span><h2>${h(row.reason)}</h2>${track(480,960,[[row.open_minute,row.end_minute]])}
       <p>${h(row.service_day)} &nbsp; <b>${hours(row.open_minute,row.end_minute)}</b> &nbsp;${h(row.code)}</p>
     </article>`).join('')}</section><aside><h2>维护记录</h2><p>归档后会反映在开放时长分母。</p>
     ${user.role==='operator'?`<form>${fields(assets)}<label>停机依据<input name="reason" minlength="3" maxlength="100" required></label>
     <button>登记停机窗</button><p role="status"></p></form>`:''}</aside></div>`
  connect(root.querySelector('form'),data=>api('/api/bench/maintenance','POST',data),()=>blocks(root,user),true)
}
