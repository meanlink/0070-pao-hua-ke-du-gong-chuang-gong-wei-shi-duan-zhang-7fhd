import {notice} from '/base.js'
import {minute} from './time.js'

export function connect(form,perform,refresh,span=false) {
  if(!form) return
  form.onsubmit=async event=>{
    event.preventDefault()
    const values=Object.fromEntries(new FormData(form))
    if (span) for(const field of ['open_minute','end_minute']) values[field]=minute(values[field])
    const buttons=[...form.querySelectorAll('button')]
    buttons.forEach(button=>button.disabled=true)
    try {
      await perform(values,event.submitter)
      await refresh()
    } catch(error) {
      notice(form.querySelector('[role=status]'),error.message,true)
    } finally {
      buttons.forEach(button=>button.disabled=false)
    }
  }
}
