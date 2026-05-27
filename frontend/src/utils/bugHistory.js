import { addBugHistory } from '@/api/bugApi'

/** 将任意值转为接口可接受的字符串（空用 ''） */
export function toHistoryValue(v) {
  if (v === undefined || v === null) return ''
  if (typeof v === 'object') {
    try {
      return JSON.stringify(v)
    } catch (e) {
      return String(v)
    }
  }
  return String(v)
}

/**
 * 写入 Bug 操作历史（POST /bug/history/add）
 * 失败不抛错、不阻断主流程，仅静默忽略（可后续接日志）
 */
export function recordBugHistory(store, { bugId, fieldName, oldValue, newValue, operatorId }) {
  if (!bugId || !fieldName) return Promise.resolve()
  const uid =
    operatorId !== undefined && operatorId !== null && operatorId !== ''
      ? operatorId
      : store && store.state && store.state.currentUser && store.state.currentUser.id
  if (uid === undefined || uid === null || uid === '') return Promise.resolve()
  return addBugHistory({
    bugId: Number(bugId),
    fieldName: String(fieldName),
    oldValue: toHistoryValue(oldValue),
    newValue: toHistoryValue(newValue),
    operatorId: Number(uid)
  }).catch(() => {})
}

/** 编辑页：与接口 fieldName 对齐的表单字段（用于对比写历史） */
export const BUG_EDIT_HISTORY_FIELDS = [
  { formKey: 'title', fieldName: 'title' },
  { formKey: 'bugType', fieldName: 'bug_type' },
  { formKey: 'severity', fieldName: 'severity' },
  { formKey: 'priority', fieldName: 'priority' },
  { formKey: 'status', fieldName: 'status' },
  { formKey: 'reporterId', fieldName: 'reporter_id' },
  { formKey: 'assigneeId', fieldName: 'assignee_id' },
  { formKey: 'moduleId', fieldName: 'module_id' },
  { formKey: 'caseId', fieldName: 'case_id' },
  { formKey: 'planId', fieldName: 'plan_id' },
  { formKey: 'environment', fieldName: 'environment' },
  { formKey: 'steps', fieldName: 'steps' },
  { formKey: 'reproduceRate', fieldName: 'reproduce_rate' }
]

export function buildBugEditBaseline(form) {
  const f = form || {}
  const o = {}
  BUG_EDIT_HISTORY_FIELDS.forEach(({ formKey }) => {
    o[formKey] = f[formKey]
  })
  return o
}

/** 对比编辑前后并逐字段写历史（仅变更字段） */
export function recordBugEditDiff(store, bugId, baseline, current) {
  if (!bugId || !baseline || !current) return Promise.resolve()
  const tasks = []
  BUG_EDIT_HISTORY_FIELDS.forEach(({ formKey, fieldName }) => {
    const ov = baseline[formKey]
    const nv = current[formKey]
    if (toHistoryValue(ov) === toHistoryValue(nv)) return
    tasks.push(recordBugHistory(store, { bugId, fieldName, oldValue: ov, newValue: nv }))
  })
  return Promise.all(tasks)
}
