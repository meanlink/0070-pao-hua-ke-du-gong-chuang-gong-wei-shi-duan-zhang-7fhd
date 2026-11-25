import {api,h} from '/base.js'
import {header,workplace} from './heading.js'
import {track} from './track.js'
import {hours} from './time.js'

export async function floor(root) {
  const machines=await api('/api/bench/machines')
  root.innerHTML=header('开放工位平面','按功能区查看设备与排班开放时段，供值班会员安排当天的使用单。')
    +`<div class="shop-floor"><section class="floor-map">${machines.map(row=>`<article>
        <span class="plate">${h(row.key)}</span><h2>${workplace(row.title,row.bay)}</h2>
        ${track(480,960,[[row.lo,row.hi]])}<p><b>${hours(row.lo,row.hi)}</b> &nbsp;${h(row.service_day)}</p>
      </article>`).join('')}</section>
      <aside><h2>开放口径</h2><p>开放时窗是计划分母。维护停机将从该时窗扣除，重叠区间只扣除一次。</p>
      <p>工位共用一台设备时，重叠使用单不会累加占用时长。</p><a href="#bulletin">查看占用率公报</a></aside></div>`
}
