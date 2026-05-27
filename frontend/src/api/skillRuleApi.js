import request from '@/utils/request'

/** Skill */
export function getSkillList(params) {
  return request({ url: '/skill/list', method: 'get', params: params || {} })
}

export function getSkillDetail(skillId) {
  return request({ url: '/skill/detail', method: 'get', params: { skillId } })
}

export function createSkill(data) {
  return request({ url: '/skill/create', method: 'post', data })
}

export function updateSkill(data) {
  return request({ url: '/skill/update', method: 'post', data })
}

export function deleteSkill(skillId) {
  return request({ url: '/skill/delete', method: 'post', data: { skillId } })
}

/** Business rule */
export function getBusinessRuleList(params) {
  return request({ url: '/business-rule/list', method: 'get', params: params || {} })
}

export function getBusinessRuleDetail(ruleId) {
  return request({ url: '/business-rule/detail', method: 'get', params: { ruleId } })
}

export function createBusinessRule(data) {
  return request({ url: '/business-rule/create', method: 'post', data })
}

export function updateBusinessRule(data) {
  return request({ url: '/business-rule/update', method: 'post', data })
}

export function deleteBusinessRule(ruleId) {
  return request({ url: '/business-rule/delete', method: 'post', data: { ruleId } })
}
