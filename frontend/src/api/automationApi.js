import request from '@/utils/request'

/** POST /automation/plan/run — 文档字段为 camelCase */
export function runAutomationPlan(data) {
  return request({
    url: '/automation/plan/run',
    method: 'post',
    data: data || {}
  })
}

/** POST /automation/case/run */
export function runAutomationCase(data) {
  return request({
    url: '/automation/case/run',
    method: 'post',
    data: data || {}
  })
}

/** GET /automation/execution/list */
export function getAutomationExecutionList(params) {
  return request({
    url: '/automation/execution/list',
    method: 'get',
    params: params || {}
  })
}

/** GET /automation/execution/detail */
export function getAutomationExecutionDetail(executionId) {
  return request({
    url: '/automation/execution/detail',
    method: 'get',
    params: { executionId }
  })
}

/** GET /automation/execution/case/list */
export function getAutomationExecutionCaseList(params) {
  return request({
    url: '/automation/execution/case/list',
    method: 'get',
    params: params || {}
  })
}

/** POST /automation/execution/poll — body 可选 { executionId }，不传则轮询所有待执行任务 */
export function postAutomationExecutionPoll(data) {
  return request({
    url: '/automation/execution/poll',
    method: 'post',
    data: data || {}
  })
}
