import request from '@/utils/request'

export function getRoleList(params) {
  return request({
    url: '/role/list',
    method: 'get',
    params: params || {}
  })
}

/** 从 /role/list 响应中取出菜单树（兼容多种 data 形态） */
export function parseMenusFromRoleListResponse(res) {
  if (!res) return []
  const raw = res.data !== undefined ? res.data : res
  if (Array.isArray(raw)) return raw
  if (raw && typeof raw === 'object') {
    if (Array.isArray(raw.menus)) return raw.menus
    if (Array.isArray(raw.menuList)) return raw.menuList
    if (Array.isArray(raw.list)) return raw.list
    if (Array.isArray(raw.items)) return raw.items
    if (Array.isArray(raw.records)) return raw.records
  }
  return []
}

export function getRolePageList(params) {
  return request({
    url: '/role/page/list',
    method: 'get',
    params: Object.assign({ pageNo: 1, pageSize: 10 }, params || {})
  })
}

export function getRoleDetail(roleId) {
  return request({
    url: '/role/detail',
    method: 'get',
    params: { roleId }
  })
}

export function createRole(data) {
  return request({
    url: '/role/create',
    method: 'post',
    data
  })
}

export function updateRole(data) {
  return request({
    url: '/role/update',
    method: 'post',
    data
  })
}

export function deleteRole(data) {
  return request({
    url: '/role/delete',
    method: 'post',
    data
  })
}

export function getRoleMenuTree(params) {
  return request({
    url: '/role/menu/tree',
    method: 'get',
    params: params || {}
  })
}

export function getRoleMenuList(roleId) {
  return request({
    url: '/role/menu/list',
    method: 'get',
    params: { roleId }
  })
}

export function assignRoleMenus(data) {
  return request({
    url: '/role/menu/assign',
    method: 'post',
    data
  })
}

export function getUserList(params) {
  return request({
    url: '/user/list',
    method: 'get',
    params: Object.assign({ pageNo: 1, pageSize: 10 }, params || {})
  })
}

export function getUserDetail(userId) {
  return request({
    url: '/user/detail',
    method: 'get',
    params: { userId }
  })
}

export function createUser(data) {
  return request({
    url: '/user/create',
    method: 'post',
    data
  })
}

export function updateUser(data) {
  return request({
    url: '/user/update',
    method: 'post',
    data
  })
}

export function deleteUser(data) {
  return request({
    url: '/user/delete',
    method: 'post',
    data
  })
}

export function getUserRoleList(userId) {
  return request({
    url: '/user/role/list',
    method: 'get',
    params: { userId }
  })
}

export function assignUserRoles(data) {
  return request({
    url: '/user/role/assign',
    method: 'post',
    data
  })
}

export function getMenuTree(params) {
  return request({
    url: '/menu/tree',
    method: 'get',
    params: params || {}
  })
}

export function getMenuDetail(menuId) {
  return request({
    url: '/menu/detail',
    method: 'get',
    params: { menuId }
  })
}

export function createMenu(data) {
  return request({
    url: '/menu/create',
    method: 'post',
    data
  })
}

export function updateMenu(data) {
  return request({
    url: '/menu/update',
    method: 'post',
    data
  })
}

export function deleteMenu(data) {
  return request({
    url: '/menu/delete',
    method: 'post',
    data
  })
}

export function getPermissionList(params) {
  return request({
    url: '/permission/list',
    method: 'get',
    params: Object.assign({ pageNo: 1, pageSize: 20 }, params || {})
  })
}

export function getPermissionDetail(permissionId) {
  return request({
    url: '/permission/detail',
    method: 'get',
    params: {
      permission_id: permissionId,
      permissionId: permissionId,
      id: permissionId
    }
  })
}

export function createPermission(data) {
  return request({
    url: '/permission/create',
    method: 'post',
    data
  })
}

export function updatePermission(data) {
  return request({
    url: '/permission/update',
    method: 'post',
    data
  })
}

export function deletePermission(data) {
  return request({
    url: '/permission/delete',
    method: 'post',
    data
  })
}

export function assignRolePermissions(data) {
  return request({
    url: '/role/permission/assign',
    method: 'post',
    data
  })
}
