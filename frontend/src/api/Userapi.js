import request from '@/utils/request'

/*注册模块*/
export function Register(data) {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}

/*登录功能*/
export function Login(data) {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  })
}

export function logout() {
  return request({
    url:'/login/out',
    method: 'get'
  })
}
//新增用户
export function userAdd(data) {
  return request({
    url: '/manageSystem/user/add',
    method: 'post',
    data
  })
}
//删除用户
export function userDelete(data) {
  return request({
    url: '/manageSystem/user/delete',
    method: 'post',
    data
  })
}
//用户列表
export function userQueryAdvance(data) {
  return request({
    url: '/manageSystem/user/queryAdvance',
    method: 'post',
    data
  })
}
//单个用户详情
export function userGetAdvance(data) {
  return request({
    url: '/manageSystem/user/getAdvance',
    method: 'post',
    data
  })
}

//修改密码
export function editPassword(data) {
  return request({
    url: '/manageSystem/user/editPassword',
    method: 'post',
    data
  })
}
