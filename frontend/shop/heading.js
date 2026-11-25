import {h} from '/base.js'

export const header=(title,body)=>`<header class="shop-header"><h1>${h(title)}</h1><p>${h(body)}</p></header>`
export const workplace=(name,zone)=>`<strong>${h(name)}</strong><small>${h(zone)}</small>`
