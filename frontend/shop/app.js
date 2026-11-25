import {mount} from '/base.js'
import {floor} from './floor.js'
import {records} from './sessions.js'
import {blocks} from './maintenance.js'
import {bulletin} from './bulletin.js'

const show={floor,records,blocks,bulletin}
mount({title:'刨花刻度 · 共创工位时段账',kicker:'松灯木工共创社 / 工位排班',
  pages:{floor:'工位平面',records:'使用单复核',blocks:'维护窗登记',bulletin:'占用率公报'},
  render:(slug,node,user)=>show[slug](node,user)})
