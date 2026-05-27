# RBAC / 用户 / 菜单管理接口文档

本文档基于当前已落地代码整理，适合直接给前端联调使用。

## 1. 通用说明

### 1.1 响应结构

成功：

```json
{
  "success": true,
  "code": 20000,
  "message": "",
  "data": {}
}
```

失败：

```json
{
  "success": false,
  "code": 40009,
  "message": "具体错误信息",
  "data": null
}
```

### 1.2 错误码使用习惯

| code  | 说明             |
| ----- | -------------- |
| 20000 | 成功             |
| 40009 | 创建类失败 / 参数校验失败 |
| 40011 | 详情查询失败         |
| 40012 | 更新 / 删除 / 分配失败 |

### 1.3 当前实现注意事项

- 用户密码字段当前直接写入 `password_hash`，还未做真正加密
- 分配类接口均为覆盖式保存
- 当前密码字段是占位实现，后续建议替换为真实 hash

***

## 2. 角色管理

### 2.1 角色列表

- 方法：`GET`
- 路径：`/role/list`

请求参数：

| 参数名      | 类型     | 必填 | 说明        |
| -------- | ------ | -- | --------- |
| keyword  | string | 否  | 角色名称模糊搜索  |
| status   | int    | 否  | 1启用 0禁用   |
| pageNo   | int    | 否  | 页码，默认1    |
| pageSize | int    | 否  | 每页条数，默认20 |

返回 `data`：

```json
{
  "list": [
    {
      "id": 1,
      "code": "admin",
      "name": "超级管理员",
      "description": "系统内置超级管理员",
      "status": 1,
      "is_system": 1,
      "created_by": 1,
      "created_time": "2025-01-01 10:00:00",
      "updated_time": "2025-01-01 10:00:00"
    }
  ],
  "total": 1
}
```

### 2.2 角色详情

- 方法：`GET`
- 路径：`/role/detail`

请求参数：

| 参数名    | 类型  | 必填 | 说明   |
| ------ | --- | -- | ---- |
| roleId | int | 是  | 角色ID |

返回：单个角色对象。

### 2.3 创建角色

- 方法：`POST`
- 路径：`/role/create`

请求体：

```json
{
  "code": "test_manager",
  "name": "测试经理",
  "description": "测试经理角色",
  "status": 1,
  "isSystem": 0,
  "createdBy": 1
}
```

返回：

```json
{
  "id": 2
}
```

### 2.4 更新角色

- 方法：`POST`
- 路径：`/role/update`

请求体：

```json
{
  "roleId": 2,
  "name": "高级测试经理",
  "description": "升级后的测试经理角色"
}
```

返回：

```json
{
  "id": 2
}
```

### 2.5 删除角色

- 方法：`POST`
- 路径：`/role/delete`

请求体：

```json
{
  "roleId": 2
}
```

返回：

```json
{
  "id": 2
}
```

***

## 3. 权限管理

### 3.1 权限列表

- 方法：`GET`
- 路径：`/permission/list`

请求参数：

| 参数名      | 类型     | 必填 | 说明       |
| -------- | ------ | -- | -------- |
| keyword  | string | 否  | 权限名称模糊搜索 |
| module   | string | 否  | 模块名      |
| status   | int    | 否  | 状态       |
| pageNo   | int    | 否  | 页码       |
| pageSize | int    | 否  | 每页条数     |

返回 `data`：

```json
{
  "list": [
    {
      "id": 1,
      "code": "user:create",
      "name": "创建用户",
      "module": "user",
      "action": "create",
      "description": "创建用户权限",
      "status": 1,
      "created_time": "2025-01-01 10:00:00",
      "updated_time": "2025-01-01 10:00:00"
    }
  ],
  "total": 1
}
```

### 3.2 权限详情

- 方法：`GET`
- 路径：`/permission/detail`
- 参数：`permissionId`

### 3.3 创建权限

- 方法：`POST`
- 路径：`/permission/create`

请求体：

```json
{
  "code": "user:create",
  "name": "创建用户",
  "module": "user",
  "action": "create",
  "description": "创建用户权限",
  "status": 1
}
```

### 3.4 更新权限

- 方法：`POST`
- 路径：`/permission/update`

### 3.5 删除权限

- 方法：`POST`
- 路径：`/permission/delete`

***

## 4. 菜单管理

### 4.1 菜单树

- 方法：`GET`
- 路径：`/menu/tree`

请求参数：

| 参数名    | 类型  | 必填 | 说明   |
| ------ | --- | -- | ---- |
| status | int | 否  | 状态过滤 |

返回 `data`：

```json
[
  {
    "id": 1,
    "parent_id": 0,
    "name": "系统管理",
    "code": "system",
    "type": 1,
    "path": "/system",
    "component": "Layout",
    "icon": "setting",
    "permission_code": null,
    "sort": 1,
    "visible": 1,
    "status": 1,
    "created_time": "2025-01-01 10:00:00",
    "updated_time": "2025-01-01 10:00:00",
    "children": [
      {
        "id": 2,
        "parent_id": 1,
        "name": "用户管理",
        "code": "user_manage",
        "type": 2,
        "path": "/system/user",
        "component": "system/user/index",
        "icon": "user",
        "permission_code": "user:list",
        "sort": 1,
        "visible": 1,
        "status": 1,
        "children": []
      }
    ]
  }
]
```

### 4.2 菜单详情

- 方法：`GET`
- 路径：`/menu/detail`
- 参数：`menuId`

### 4.3 创建菜单

- 方法：`POST`
- 路径：`/menu/create`

请求体：

```json
{
  "parentId": 1,
  "name": "角色管理",
  "code": "role_manage",
  "type": 2,
  "path": "/system/role",
  "component": "system/role/index",
  "icon": "peoples",
  "permissionCode": "role:list",
  "sort": 2,
  "visible": 1,
  "status": 1
}
```

### 4.4 更新菜单

- 方法：`POST`
- 路径：`/menu/update`

### 4.5 删除菜单

- 方法：`POST`
- 路径：`/menu/delete`

***

## 5. 角色权限分配

### 5.1 查询角色权限

- 方法：`GET`
- 路径：`/role/permission/list`
- 参数：`roleId`

返回：

```json
{
  "permissionIds": [1, 2, 3]
}
```

### 5.2 分配角色权限

- 方法：`POST`
- 路径：`/role/permission/assign`

请求体：

```json
{
  "roleId": 2,
  "permissionIds": [1, 2, 3, 4]
}
```

返回：

```json
{
  "id": 2
}
```

***

## 6. 角色菜单分配

### 6.1 查询角色菜单

- 方法：`GET`
- 路径：`/role/menu/list`
- 参数：`roleId`

返回：

```json
{
  "menuIds": [1, 2, 3, 4]
}
```

### 6.2 分配角色菜单

- 方法：`POST`
- 路径：`/role/menu/assign`

请求体：

```json
{
  "roleId": 2,
  "menuIds": [1, 2, 10, 11]
}
```

返回：

```json
{
  "id": 2
}
```

***

## 7. 用户管理

### 7.1 用户列表

- 方法：`GET`
- 路径：`/user/list`

请求参数：

| 参数名      | 类型     | 必填 | 说明      |
| -------- | ------ | -- | ------- |
| keyword  | string | 否  | 用户名模糊搜索 |
| status   | int    | 否  | 状态      |
| pageNo   | int    | 否  | 页码      |
| pageSize | int    | 否  | 每页条数    |

返回 `data`：

```json
{
  "list": [
    {
      "id": 1,
      "username": "admin",
      "real_name": "管理员",
      "mobile": "13800000000",
      "email": "admin@test.com",
      "avatar": "",
      "status": 1,
      "last_login_time": "2025-01-01 10:00:00",
      "created_by": 1,
      "created_time": "2025-01-01 10:00:00",
      "updated_time": "2025-01-01 10:00:00",
      "role_ids": [1, 2],
      "role_names": ["管理员", "测试经理"]
    }
  ],
  "total": 1
}
```

### 7.2 用户详情

- 方法：`GET`
- 路径：`/user/detail`
- 参数：`userId`

返回会额外包含：

```json
{
  "role_ids": [1, 2]
}
```

### 7.3 创建用户

- 方法：`POST`
- 路径：`/user/create`

请求体：

```json
{
  "username": "zhangsan",
  "password": "123456",
  "realName": "张三",
  "mobile": "13800001111",
  "email": "zhangsan@test.com",
  "avatar": "",
  "status": 1,
  "createdBy": 1
}
```

返回：

```json
{
  "id": 3
}
```

### 7.4 更新用户

- 方法：`POST`
- 路径：`/user/update`

### 7.5 删除用户

- 方法：`POST`
- 路径：`/user/delete`

***

## 8. 用户角色分配

### 8.1 查询用户角色

- 方法：`GET`
- 路径：`/user/role/list`
- 参数：`userId`

返回：

```json
{
  "roleIds": [1, 2]
}
```

### 8.2 分配用户角色

- 方法：`POST`
- 路径：`/user/role/assign`

请求体：

```json
{
  "userId": 10,
  "roleIds": [2, 3]
}
```

响应：

```json
{
  "id": 10
}
```

***

## 9. 认证接口

### 9.1 注册

- 方法：`POST`
- 路径：`/auth/register`

请求体：

```json
{
  "username": "zhangsan",
  "password": "123456",
  "realName": "张三",
  "mobile": "13800001111",
  "email": "zhangsan@test.com",
  "avatar": "",
  "createdBy": 1
}
```

请求参数说明：

| 参数名       | 类型     | 必填 | 说明                          |
| --------- | ------ | -- | --------------------------- |
| username  | string | 是  | 登录用户名                       |
| password  | string | 是  | 登录密码，当前直接写入 `password_hash` |
| realName  | string | 否  | 真实姓名                        |
| mobile    | string | 否  | 手机号                         |
| email     | string | 否  | 邮箱                          |
| avatar    | string | 否  | 头像                          |
| createdBy | int    | 否  | 创建人                         |

成功返回：

```json
{
  "id": 11
}
```

失败场景：

- `username、password 为必传参数`
- `用户名已存在！`

### 9.2 登录

- 方法：`POST`
- 路径：`/auth/login`

请求体：

```json
{
  "username": "zhangsan",
  "password": "123456"
}
```

请求参数说明：

| 参数名      | 类型     | 必填 | 说明    |
| -------- | ------ | -- | ----- |
| username | string | 是  | 登录用户名 |
| password | string | 是  | 登录密码  |

成功返回 `data`：

```json
{
  "id": 11,
  "username": "zhangsan",
  "real_name": "张三",
  "mobile": "13800001111",
  "email": "zhangsan@test.com",
  "avatar": "",
  "status": 1,
  "last_login_time": null,
  "created_by": 1,
  "created_time": "2025-01-01 10:00:00",
  "updated_time": "2025-01-01 10:00:00",
  "role_ids": [2, 3]
}
```

失败场景：

- `username、password 为必传参数`
- `用户名或密码错误！`
- `用户已禁用！`

登录成功额外返回：

| 字段                          | 类型     | 说明                      |
| --------------------------- | ------ | ----------------------- |
| token                       | string | 登录令牌，存入 Redis           |
| token\_type                 | string | 固定为 `Bearer`            |
| expires\_in                 | int    | token 过期时间，单位秒，当前为 7200 |
| refresh\_threshold\_seconds | int    | 自动续期阈值，单位秒，当前为 1800     |
| refresh\_mechanism          | string | 刷新机制说明                  |

当前 token 机制：

- token 存储位置：Redis
- Redis key 前缀：`effekt:token:`
- token 过期时间：`7200` 秒（2小时）
- 刷新机制：访问任意需要登录的接口时，如果 token 剩余有效期小于 `1800` 秒，则自动续期到完整 2 小时
- 请求头支持：
  - `accessToken`
  - `accesstoken`
  - `Authorization: Bearer <token>`

> 当前登录接口已返回 token、过期时间和刷新机制说明。

***

## 10. 一组联调示例

### 9.1 创建角色

```http
POST /role/create
Content-Type: application/json
```

```json
{
  "code": "tester",
  "name": "测试人员",
  "description": "普通测试角色",
  "status": 1,
  "isSystem": 0
}
```

### 9.2 创建权限

```json
{
  "code": "case:list",
  "name": "查看用例列表",
  "module": "case",
  "action": "list",
  "description": "查看测试用例列表",
  "status": 1
}
```

### 9.3 创建菜单

```json
{
  "parentId": 1,
  "name": "权限管理",
  "code": "permission_manage",
  "type": 2,
  "path": "/system/permission",
  "component": "system/permission/index",
  "icon": "lock",
  "permissionCode": "permission:list",
  "sort": 3,
  "visible": 1,
  "status": 1
}
```

### 9.4 给角色分配权限

```json
{
  "roleId": 5,
  "permissionIds": [1, 2, 3, 4]
}
```

### 9.5 给角色分配菜单

```json
{
  "roleId": 5,
  "menuIds": [1, 2, 8, 9]
}
```

### 9.6 创建用户

```json
{
  "username": "lisi",
  "password": "123456",
  "realName": "李四",
  "mobile": "13800002222",
  "email": "lisi@test.com",
  "status": 1
}
```

### 10.7 给用户分配角色

```json
{
  "userId": 10,
  "roleIds": [5]
}
```

### 10.8 注册

```json
{
  "username": "new_user",
  "password": "123456",
  "realName": "新用户",
  "mobile": "13800009999",
  "email": "new_user@test.com"
}
```

### 10.9 登录

```json
{
  "username": "new_user",
  "password": "123456"
}
```

### 10.10 鉴权说明

请求受保护接口时，请在请求头中携带以下任意一种：

```text
accessToken: <token>
```

或

```text
accesstoken: <token>
```

或

```text
Authorization: Bearer <token>
```

当前机制：

- token 存 Redis
- 默认有效期：2 小时
- 剩余有效期小于 30 分钟时，访问受保护接口会自动续期
- 注册、登录接口不需要 token
- 其他接口已逐步接入登录鉴权与权限限制

***

## 11. 当前初始化 SQL 已包含的业务菜单

已补入以下可直接录入的菜单数据：

### 系统管理

- `system` 系统管理
- `role_manage` 角色管理
- `user_manage` 用户管理
- `permission_manage` 权限管理
- `menu_manage` 菜单管理

### 测试平台

- `test_platform` 测试平台
- `product_manage` 产品管理
- `project_manage` 项目管理
- `case_manage` 用例管理
- `plan_manage` 测试计划
- `report_manage` 测试报告

### 造数工具

- `data_tools` 造数工具
- `data_builder_manage` 数据库造数
- `data_factory_manage` 造数工厂

如果后续你要，我可以继续补：

1. Swagger/OpenAPI 版本
2. Apifox / Postman 导入版
3. 初始化权限菜单角色的更完整种子数据

