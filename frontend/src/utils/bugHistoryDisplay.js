import {
  STATUS_MAP,
  PRIORITY_MAP,
  SEVERITY_MAP,
  BUG_TYPE_MAP,
  formatBugType,
  formatReproduceRate
} from '@/utils/bugMaps'

/** 历史记录 field_name / fieldName → 中文 */
const FIELD_NAME_CN = {
  status: '状态',
  assignee_id: '当前指派',
  reporter_id: '创建人',
  module_id: '模块',
  product_id: '产品',
  project_id: '项目',
  priority: '优先级',
  severity: '严重程度',
  bug_type: '类型',
  title: '标题',
  environment: '环境',
  case_id: '关联用例',
  plan_id: '关联计划',
  steps: '复现步骤',
  solution: '解决方案',
  resolve_version: '解决版本',
  resolve_comment: '解决备注',
  comment: '备注',
  create: '创建',
  delete: '删除',
  description: '描述',
  user_id: '用户',
  is_auto: '自动化',
  reproduce_rate: '复现率',
  resolved_by: '解决人'
}

const SOLUTION_CN = {
  by_design: '设计如此',
  duplicate_bug: '重复Bug',
  external_reason: '外部原因',
  solution_resolved: '已解决',
  cannot_reproduce: '无法重现',
  deferred: '延期处理',
  wont_fix: '不予解决'
}

const RESOLVE_VERSION_CN = {
  trunk: '主干',
  current_sprint: '当前迭代',
  next: '下一版本'
}

function stripHtmlBrief(html, maxLen) {
  if (html == null || html === '') return ''
  const text = String(html)
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
  if (!text) return '（富文本）'
  if (maxLen && text.length > maxLen) return text.slice(0, maxLen) + '…'
  return text
}

function toSnakeFieldKey(name) {
  const s = String(name || '').trim()
  if (!s) return ''
  return s
    .replace(/([a-z\d])([A-Z])/g, '$1_$2')
    .replace(/([A-Z]+)([A-Z][a-z])/g, '$1_$2')
    .toLowerCase()
    .replace(/^_+/, '')
    .replace(/_+/g, '_')
}

/** 与 BUG_EDIT_HISTORY_FIELDS / 接口 fieldName 对齐的 snake_case key */
export function normalizeBugHistoryFieldKey(name) {
  const snake = toSnakeFieldKey(name)
  if (!snake) return ''
  const compact = snake.replace(/_/g, '')
  const alias = {
    assigneeid: 'assignee_id',
    reporterid: 'reporter_id',
    moduleid: 'module_id',
    productid: 'product_id',
    projectid: 'project_id',
    caseid: 'case_id',
    planid: 'plan_id',
    bugtype: 'bug_type',
    reproducerate: 'reproduce_rate',
    resolvedby: 'resolved_by',
    userid: 'user_id',
    isauto: 'is_auto',
    resolveversion: 'resolve_version',
    resolvecomment: 'resolve_comment',
    oldvalue: 'old_value',
    newvalue: 'new_value',
    fieldname: 'field_name'
  }
  return alias[compact] || snake
}

export function formatBugHistoryFieldName(name) {
  const k = normalizeBugHistoryFieldKey(name)
  if (!k) return '-'
  return FIELD_NAME_CN[k] || String(name || '').trim() || '-'
}

/**
 * 按字段将历史 old/new 转为中文展示（未知枚举则原样返回）
 */
export function formatBugHistoryCellValue(fieldName, value) {
  const fn = normalizeBugHistoryFieldKey(fieldName)
  const raw = value
  if (raw === undefined || raw === null || raw === '') return '（空）'

  const s = String(raw).trim()

  switch (fn) {
    case 'status':
      return STATUS_MAP[Number(s)] != null ? STATUS_MAP[Number(s)] : s
    case 'priority':
      return PRIORITY_MAP[Number(s)] != null ? PRIORITY_MAP[Number(s)] : s
    case 'severity':
      return SEVERITY_MAP[Number(s)] != null ? SEVERITY_MAP[Number(s)] : s
    case 'bug_type':
      return BUG_TYPE_MAP[Number(s)] != null ? BUG_TYPE_MAP[Number(s)] : formatBugType(Number(s))
    case 'solution':
      return SOLUTION_CN[s] || s
    case 'resolve_version':
      return RESOLVE_VERSION_CN[s] || s
    case 'resolve_comment':
    case 'comment':
      return stripHtmlBrief(raw, 160)
    case 'create':
    case 'delete':
      if (s === '0' || s === '1') return s === '1' ? '是' : '否'
      return s
    case 'steps':
      return stripHtmlBrief(raw, 120)
    case 'reproduce_rate':
      return formatReproduceRate(s)
    case 'resolved_by':
      return s
    default:
      return s
  }
}

/** 解决弹窗历史列表用：单行描述 */
export function formatBugHistoryLineText(h) {
  const fn = h.field_name || h.fieldName || ''
  var ov = h.old_value
  if (ov === undefined || ov === null) ov = h.oldValue
  var nv = h.new_value
  if (nv === undefined || nv === null) nv = h.newValue
  const op = h.operator_id || h.operatorId || h.operator_name || h.operatorName || ''
  const label = formatBugHistoryFieldName(fn)
  const o = formatBugHistoryCellValue(fn, ov)
  const n = formatBugHistoryCellValue(fn, nv)
  return `${label}：${o} → ${n}（操作人 ${op}）`
}
