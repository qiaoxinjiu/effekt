# 测试 Skills 与业务规则接口文档

## 1. 基础说明

接口前缀：`/it/api`

统一响应：

```json
{
  "code": 20000,
  "msg": "success",
  "data": {}
}
```

鉴权：需要登录态 token。

建议请求头：

```http
Authorization: Bearer ${token}
```

也兼容：

```http
accessToken: ${token}
```

***

## 2. 枚举

### 2.1 Skill 类型 skill\_type

| 值  | 含义     |
| -- | ------ |
| 1  | 通用测试策略 |
| 2  | 历史缺陷模式 |
| 3  | 边界场景   |
| 4  | 接口测试   |
| 5  | UI 测试  |
| 6  | 性能测试   |
| 7  | 安全测试   |
| 8  | 数据一致性  |
| 9  | 并发/幂等  |
| 99 | 其他     |

### 2.2 风险等级 risk\_level

| 值 | 含义   |
| - | ---- |
| 0 | 高风险  |
| 1 | 中高风险 |
| 2 | 中风险  |
| 3 | 低风险  |

### 2.3 业务规则优先级 priority

| 值 | 含义    |
| - | ----- |
| 0 | 高优先级  |
| 1 | 中高优先级 |
| 2 | 中优先级  |
| 3 | 低优先级  |

### 2.4 状态 status

| 值 | 含义 |
| - | -- |
| 1 | 启用 |
| 2 | 停用 |
| 3 | 草稿 |

***

## 3. Skill 接口

### 3.1 创建 Skill

```http
POST /it/api/skill/create
```

权限：`skill:create`

请求体：

```json
{
  "projectId": 1,
  "moduleId": 10,
  "name": "支付金额边界校验",
  "description": "用于支付金额相关需求的边界测试生成",
  "skillType": 3,
  "riskLevel": 0,
  "tags": ["支付", "金额", "边界"],
  "status": 1
}
```

参数：

| 字段          | 类型        | 必填 | 说明 |
| ------------- | ----------- | ---- | ---- |
| projectId     | number      | 是   | 项目 ID |
| moduleId      | number      | 否   | 模块 ID |
| name          | string      | 是   | Skill 名称 |
| description   | string      | 否   | 用户补充描述，会作为大模型生成 Skill 内容的输入 |
| skillType     | number      | 否   | Skill 类型，未传时默认 1；大模型也可能根据内容修正 |
| riskLevel     | number      | 否   | 风险等级，未传时默认 2；大模型也可能根据内容修正 |
| tags          | string\[]   | 否   | 初始标签数组，大模型可能补全 |
| status        | number      | 否   | 状态，默认 1 |

说明：

- `code` 不需要前端传，后端自动生成项目内唯一编码。
- `triggerCondition` 不需要前端传，后端默认使用当前 AI 生成用例的触发条件。
- `outputSpec` 不需要前端传，后端默认使用当前 AI 生成用例的输出规范。
- `reasoningPath` 不需要前端传，后端会调用大模型并根据 `config/skills/skill-creator/SKILL.md` 规则生成。
- `ownerId` 不需要前端传，后端默认取当前登录人 ID。
- 创建成功后，后端会在 `config/skills/{产品名称}/{项目名称}/{模块名称}/{Skill名称}/SKILL.md` 生成 Skill 文件。
- 数据库会保存生成文件路径到 `skill_file_path`。

成功响应：

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "id": 1
  }
}
```

常见失败：

```json
{
  "code": 40009,
  "msg": "projectId、name 为必传参数"
}
```

```json
{
  "code": 40009,
  "msg": "AI生成 Skill 内容失败: xxx"
}
```

***

### 3.2 更新 Skill

```http
POST /it/api/skill/update
```

权限：`skill:update`

请求体：

```json
{
  "skillId": 1,
  "name": "支付金额边界校验",
  "description": "更新后的描述",
  "triggerCondition": "更新后的触发条件",
  "reasoningPath": "更新后的推理路径",
  "outputSpec": "更新后的输出规范",
  "skillType": 3,
  "riskLevel": 0,
  "tags": ["支付", "金额", "边界", "参数校验"],
  "status": 1,
  "ownerId": 8
}
```

说明：

- 当前接口不支持更新 `code`。
- 更新成功后，后端会根据更新后的 Skill 内容重新创建 `SKILL.md` 文件。
- 新文件路径会同步更新到数据库 `skill_file_path`。
- 数据库更新成功后会删除原 Skill 文件夹。
- 如果数据库更新失败，后端会删除新创建的文件夹并保留旧数据库记录和旧文件，避免数据库与文件不一致。

成功响应：

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "id": 1
  }
}
```

***

### 3.3 删除 Skill

```http
POST /it/api/skill/delete
```

权限：`skill:delete`

请求体：

```json
{
  "skillId": 1
}
```

说明：软删除，设置 `is_delete = 1`，并删除该 Skill 对应的 `config/skills/{产品名称}/{项目名称}/{模块名称}/{Skill名称}` 文件夹。

成功响应：

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "id": 1
  }
}
```

***

### 3.4 Skill 详情

```http
GET /it/api/skill/detail?skillId=1
```

权限：`skill:detail`

成功响应：

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "id": 1,
    "project_id": 1,
    "module_id": 10,
    "name": "支付金额边界校验",
    "code": "PAY_AMOUNT_BOUNDARY",
    "description": "用于支付金额相关需求的边界测试生成",
    "trigger_condition": "需求中出现支付、金额、扣款、退款、余额等关键词时触发",
    "reasoning_path": "识别金额字段，构造最小值、最大值、0、负数、小数精度、超限金额等场景",
    "output_spec": "必须覆盖正常金额、0元、负数、超大金额、小数精度、余额不足",
    "skill_file_path": "D:\\zhyy\\effekt-interface\\config\\skills\\产品A\\项目A\\支付模块\\支付金额边界校验\\SKILL.md",
    "skill_type": 3,
    "risk_level": 0,
    "tags": ["支付", "金额", "边界"],
    "status": 1,
    "owner_id": 8,
    "created_by": 6,
    "usage_count": 0,
    "is_delete": 0,
    "created_time": "2025-09-20 12:00:00",
    "updated_time": "2025-09-20 12:00:00"
  }
}
```

***

### 3.5 Skill 列表

```http
GET /it/api/skill/list
```

权限：`skill:list`

Query 参数：

| 参数        | 类型     | 必填 | 说明                                          |
| --------- | ------ | -- | ------------------------------------------- |
| pageNo    | number | 否  | 页码，默认 1                                     |
| pageSize  | number | 否  | 每页数量，默认 20                                  |
| projectId | number | 否  | 项目 ID                                       |
| moduleId  | number | 否  | 模块 ID                                       |
| status    | number | 否  | 状态                                          |
| skillType | number | 否  | Skill 类型                                    |
| riskLevel | number | 否  | 风险等级                                        |
| keyword   | string | 否  | 搜索 name/code/description/trigger\_condition |
| tag       | string | 否  | 单个标签过滤                                      |

请求示例：

```http
GET /it/api/skill/list?pageNo=1&pageSize=20&projectId=1&moduleId=10&keyword=支付&status=1
```

成功响应：

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "project_id": 1,
        "module_id": 10,
        "name": "支付金额边界校验",
        "code": "PAY_AMOUNT_BOUNDARY",
        "description": "用于支付金额相关需求的边界测试生成",
        "trigger_condition": "需求中出现支付、金额、扣款、退款、余额等关键词时触发",
        "reasoning_path": "识别金额字段...",
        "output_spec": "必须覆盖正常金额...",
        "skill_file_path": "D:\\zhyy\\effekt-interface\\config\\skills\\产品A\\项目A\\支付模块\\支付金额边界校验\\SKILL.md",
        "skill_type": 3,
        "risk_level": 0,
        "tags": ["支付", "金额", "边界"],
        "status": 1,
        "owner_id": 8,
        "usage_count": 0,
        "created_time": "2025-09-20 12:00:00",
        "updated_time": "2025-09-20 12:00:00"
      }
    ],
    "total": 1
  }
}
```

***

## 4. Business Rule 接口

### 4.1 创建业务规则

```http
POST /it/api/business-rule/create
```

权限：`business-rule:create`

请求体：

```json
{
  "projectId": 1,
  "moduleId": 10,
  "name": "支付金额必须大于 0",
  "description": "用于支付、充值、扣款、退款等金额输入场景的参数校验规则",
  "priority": 0,
  "tags": ["支付", "金额", "参数校验"],
  "status": 1
}
```

参数：

| 字段        | 类型        | 必填 | 说明 |
| ----------- | ----------- | ---- | ---- |
| projectId   | number      | 是   | 项目 ID |
| moduleId    | number      | 否   | 模块 ID |
| name        | string      | 是   | 规则名称 |
| description | string      | 否   | 用户补充描述，会作为大模型生成规则内容的输入 |
| priority    | number      | 否   | 优先级，默认 2；大模型也可能根据内容修正 |
| tags        | string\[]   | 否   | 初始标签数组，大模型可能补全 |
| status      | number      | 否   | 状态，默认 1 |

说明：

- `ruleCode` 不需要前端传，后端自动生成项目内唯一编码。
- `ruleContent`、`applicableScene`、`example` 不需要前端传，后端会调用大模型生成。
- `ownerId` 不需要前端传，后端默认取当前登录人 ID。
- 创建成功后，后端会在 `config/rules/{产品名称}/{项目名称}/{模块名称}/{规则名称}/RULE.md` 生成业务规则文件。
- 数据库会保存生成文件路径到 `rule_file_path`。

成功响应：

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "id": 1
  }
}
```

***

### 4.2 更新业务规则

```http
POST /it/api/business-rule/update
```

权限：`business-rule:update`

请求体：

```json
{
  "ruleId": 1,
  "name": "支付金额必须大于 0",
  "ruleContent": "支付金额必须大于 0，等于 0 或小于 0 时接口应返回参数错误",
  "applicableScene": "支付、充值、扣款、退款金额输入",
  "example": "amount=0，预期返回金额必须大于0",
  "priority": 0,
  "tags": ["支付", "金额", "参数校验"],
  "status": 1,
  "ownerId": 8
}
```

说明：

- 当前接口不支持更新 `ruleCode`。
- 更新成功后，后端会根据更新后的业务规则内容重新创建 `RULE.md` 文件。
- 新文件路径会同步更新到数据库 `rule_file_path`。
- 数据库更新成功后会删除原业务规则文件夹。
- 如果数据库更新失败，后端会删除新创建的文件夹并保留旧数据库记录和旧文件，避免数据库与文件不一致。

成功响应：

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "id": 1
  }
}
```

***

### 4.3 删除业务规则

```http
POST /it/api/business-rule/delete
```

权限：`business-rule:delete`

请求体：

```json
{
  "ruleId": 1
}
```

说明：软删除，设置 `is_delete = 1`，并删除该业务规则对应的 `config/rules/{产品名称}/{项目名称}/{模块名称}/{规则名称}` 文件夹。

***

### 4.4 业务规则详情

```http
GET /it/api/business-rule/detail?ruleId=1
```

权限：`business-rule:detail`

成功响应：

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "id": 1,
    "project_id": 1,
    "module_id": 10,
    "name": "支付金额必须大于 0",
    "rule_code": "PAY_AMOUNT_GT_ZERO",
    "rule_content": "支付金额必须大于 0，等于 0 或小于 0 时接口应返回参数错误",
    "applicable_scene": "支付、充值、扣款、退款金额输入",
    "example": "amount=0，预期返回金额必须大于0",
    "rule_file_path": "D:\\zhyy\\effekt-interface\\config\\rules\\产品A\\项目A\\支付模块\\支付金额必须大于 0\\RULE.md",
    "priority": 0,
    "tags": ["支付", "金额", "参数校验"],
    "status": 1,
    "owner_id": 8,
    "created_by": 6,
    "usage_count": 0,
    "is_delete": 0,
    "created_time": "2025-09-20 12:00:00",
    "updated_time": "2025-09-20 12:00:00"
  }
}
```

***

### 4.5 业务规则列表

```http
GET /it/api/business-rule/list
```

权限：`business-rule:list`

Query 参数：

| 参数        | 类型     | 必填 | 说明                                                 |
| --------- | ------ | -- | -------------------------------------------------- |
| pageNo    | number | 否  | 页码，默认 1                                            |
| pageSize  | number | 否  | 每页数量，默认 20                                         |
| projectId | number | 否  | 项目 ID                                              |
| moduleId  | number | 否  | 模块 ID                                              |
| status    | number | 否  | 状态                                                 |
| priority  | number | 否  | 优先级                                                |
| keyword   | string | 否  | 搜索 name/rule\_code/rule\_content/applicable\_scene |
| tag       | string | 否  | 单个标签过滤                                             |

请求示例：

```http
GET /it/api/business-rule/list?pageNo=1&pageSize=20&projectId=1&moduleId=10&keyword=金额&status=1
```

成功响应：

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "project_id": 1,
        "module_id": 10,
        "name": "支付金额必须大于 0",
        "rule_code": "PAY_AMOUNT_GT_ZERO",
        "rule_content": "支付金额必须大于 0，等于 0 或小于 0 时接口应返回参数错误",
        "applicable_scene": "支付、充值、扣款、退款金额输入",
        "example": "amount=0，预期返回金额必须大于0",
        "priority": 0,
        "tags": ["支付", "金额", "参数校验"],
        "status": 1,
        "owner_id": 8,
        "usage_count": 0,
        "created_time": "2025-09-20 12:00:00",
        "updated_time": "2025-09-20 12:00:00"
      }
    ],
    "total": 1
  }
}
```

***

## 5. 调用示例

### 5.1 curl 创建 Skill

```bash
curl -X POST 'http://localhost:5010/it/api/skill/create' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your-token' \
  -d '{
    "projectId": 1,
    "name": "支付金额边界校验",
    "code": "PAY_AMOUNT_BOUNDARY",
    "triggerCondition": "需求中出现支付、金额、扣款、退款、余额等关键词时触发",
    "skillType": 3,
    "riskLevel": 0,
    "tags": ["支付", "金额", "边界"]
  }'
```

### 5.2 curl 创建业务规则

```bash
curl -X POST 'http://localhost:5010/it/api/business-rule/create' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your-token' \
  -d '{
    "projectId": 1,
    "name": "支付金额必须大于 0",
    "ruleCode": "PAY_AMOUNT_GT_ZERO",
    "ruleContent": "支付金额必须大于 0，等于 0 或小于 0 时接口应返回参数错误",
    "priority": 0,
    "tags": ["支付", "金额", "参数校验"]
  }'
```

***

## 6. 注意事项

1. 返回字段是后端数据库下划线风格，例如 `project_id`、`created_time`。
2. `tags` 是数组，创建和更新时必须传数组。
3. 删除是软删除。
4. Skill 的 `code` 和业务规则的 `ruleCode` 当前不支持更新。
5. 本次接口只做 Skills / Rules 管理，暂未接入 PRD AI 生成用例链路。

