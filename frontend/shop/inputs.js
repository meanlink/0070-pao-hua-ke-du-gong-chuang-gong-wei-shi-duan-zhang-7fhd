import {h} from '/base.js'

export const fields=assets=>`<label>单号<input name="code" pattern="[A-Z0-9-]{3,24}" required></label>
  <label>设备<select name="machine">${assets.map(row=>`<option value="${h(row.key)}">${h(row.title)}</option>`).join('')}</select></label>
  <label>日期<input type="date" name="service_day" value="${h(assets[0]?.service_day)}" required></label>
  <label>开始<input type="time" name="open_minute" required></label>
  <label>结束<input type="time" name="end_minute" required></label>`
