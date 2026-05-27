import request from '@/utils/request'

// 造数任务列表
export function ItApiList(params) {
  return request({
    url: '/list',
    method: 'get',
    params
  })
}

// 执行造数任务
export function ItApiRun(data) {
  return request({
    url: '/execute',
    method: 'post',
    data
  })
}

// 新增/修改造数任务
export function ItApiCreate(data) {
  return request({
    url: '/create',
    method: 'post',
    data
  })
}

// 造数任务详情
export function ItApiDetail(params) {
  return request({
    url: '/detail',
    method: 'get',
    params
  })
}

// 删除造数任务
export function ItApiDelete(data) {
  return request({
    url: '/delete',
    method: 'post',
    data
  })
}

/*造数基础信息模块*/
//对方法的请求参数进行新增获取修改
export function DataAdd(data) {
  return request({
    url: '/data-tools/db-builder/info/add',
    method: 'post',
    data
  })
}

//刪除造数基本信息
export function DataDelete(data) {
  return request({
    url: '/data-tools/db-builder/detail/delete',
    method: 'post',
    data
  })
}

//接口请求参数列表页查询
export function DataQuery(data) {
  return request({
    url: '/data-tools/db-builder/info/page',
    method: 'post',
    data
  })
}

//返回待编辑造数请求信息 (详情页)
export function DataAdvance(data) {
  return request({
    url: '/data-tools/db-builder/info/getAdvance',
    method: 'post',
    data
  })
}

// 重新获取eureka的ip地址
export function getEureka(data) {
  return request({
    url: '/get/eureka',
    method: 'post',
    data
  })
}
// 重新获取master代码
export function getGitPull(data) {
  return request({
    url: '/get/pull/git',
    method: 'post',
    data
  })
}

/*造数请求参数模块*/
//刪除造数请求参数信息
export function InfoDelete(data) {
  return request({
    url: '/data-tools/db-builder/info/delete',
    method: 'post',
    data
  })
}

//列表查询造数请求参数信息
export function InfoQuery(data) {
  return request({
    url: '/data-tools/db-builder/detail/page',
    method: 'post',
    data
  })
}

//查找出全部的可用方法与描述进行录库
export function InfoScrapy(data) {
  return request({
    url: '/data-tools/db-builder/detail/scrapy',
    method: 'post',
    data
  })
}

//运行造数
export function RunCreateData(data) {
  return request({
    url: '/data-tools/db-builder/run',
    method: 'post',
    data
  })
}

/*造数结果模块*/
//造数结果列表页查询
export function ResultQuery(data) {
  return request({
    url: '/data-tools/db-builder/result/page',
    method: 'post',
    data
  })
}

//返回待编辑造数结果 (详情页)
export function ResultAdvance(data) {
  return request({
    url: '/data-tools/db-builder/result/getAdvance',
    method: 'post',
    data
  })
}

/*造数数据字典*/
//增加数据字典
export function DictAdd(data) {
  return request({
    url: '/add/dict/data',
    method: 'post',
    data
  })
}

//查询数据字典
export function DictQuery(data) {
  return request({
    url: '/dict/data/page',
    method: 'post',
    data
  })
}

//抓取入库
export function ScrapyDetail(data) {
  return request({
    url: '/data-tools/db-builder/detail/scrapy',
    method: 'post',
    data
  })
}

/*菜单相关*/
//获取一级菜单名称
export function GetMenu(data) {
  return request({
    url: '/get/menu/name',
    method: 'post',
    data
  })
}
//获取业务线与业务名称
export function GetTeam(data) {
  return request({
    url: '/api/get/team/name',
    method: 'post',
    data
  })
}
