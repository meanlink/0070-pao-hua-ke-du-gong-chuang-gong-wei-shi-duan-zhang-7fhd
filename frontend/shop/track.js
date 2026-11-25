import {hours} from './time.js'

const position=(start,end,range)=>`left:${100*(range[0]-start)/(end-start)}%;width:${100*(range[1]-range[0])/(end-start)}%`

export function track(start,end,windows) {
  return `<div class="worked" title="${hours(start,end)}"><span class="axis"></span>${windows.map(
    range=>`<span class="window" style="${position(start,end,range)}" title="${hours(...range)}"></span>`).join('')}</div>`
}
