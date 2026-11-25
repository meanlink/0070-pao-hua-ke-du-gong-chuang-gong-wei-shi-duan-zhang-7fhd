import {h,badge} from '/base.js'
import {hours,labels} from './time.js'

export function sessionRows(items,reviewer) {
  return items.map(row=>`<tr><td>${h(row.code)}<small>${h(row.service_day)}</small></td><td>${h(row.machine)}</td>
    <td>${h(row.crew)}</td><td>${hours(row.open_minute,row.end_minute)}</td>
    <td>${badge(labels[row.decision],row.decision)}${reviewer&&row.decision==='logged'? `<form data-session="${h(row.code)}">
    <button name="verdict" value="counted">确认</button><button class="quiet" name="verdict" value="void">冲销</button><small role="status"></small></form>`:''}</td></tr>`).join('')
}
