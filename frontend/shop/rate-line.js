import {h} from '/base.js'
import {workplace} from './heading.js'
import {track} from './track.js'

export function rateLine(row) {
  return `<li class="rate-line"><div>${workplace(row.title,row.bay)}</div>
    <div class="rate-span">${track(480,960,row.available_windows)}${track(480,960,row.occupied_windows)}</div>
    <div><b>${row.used} / ${row.available}</b><small>占用 / 可用（分钟）</small></div>
    <b class="large-rate">${row.pct===null?'—':h(row.pct)+'%'}</b><div><b>${row.maintenance}</b><small>维护分钟</small></div></li>`
}
