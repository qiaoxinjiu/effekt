# 自动化执行接口文档

## 1. 基础说明

- 接口前缀：`/it/api`
- 鉴权方式：沿用现有登录鉴权，前端请求需携带 token
- 返回格式：沿用现有项目统一返回结构

### 成功返回示例

```json
{
  "code": 20000,
  "msg": "success",
  "data": {}
}
```

### 失败返回示例

```json
{
  "code": 40009,
  "msg": "参数错误",
  "data": null
}
```

***

## 2. 状态枚举

### 2.1 执行主单状态 `status`

| 值 | 含义   |
| - | ---- |
| 0 | 待触发  |
| 1 | 触发中  |
| 2 | 排队中  |
| 3 | 执行中  |
| 4 | 成功   |
| 5 | 失败   |
| 6 | 已取消  |
| 7 | 触发失败 |
| 8 | 回调异常 |

### 2.2 执行明细状态 `status`

| 值 | 含义  |
| - | --- |
| 0 | 待执行 |
| 1 | 执行中 |
| 2 | 通过  |
| 3 | 失败  |
| 4 | 阻塞  |
| 5 | 跳过  |
| 6 | 未找到 |
| 7 | 已取消 |

### 2.3 触发类型 `trigger_type`

| 值 | 含义   |
| - | ---- |
| 1 | 单条执行 |
| 2 | 计划执行 |

### 2.4 执行模式 `run_mode`

| 值 | 含义 |
| - | -- |
| 1 | 串行 |
| 2 | 并行 |

***

## 3. 接口清单

| 接口                                | 方法   | 说明        |
| --------------------------------- | ---- | --------- |
| `/automation/case/run`            | POST | 单条自动化用例执行 |
| `/automation/plan/run`            | POST | 计划自动化用例执行 |
| `/automation/execution/list`      | GET  | 自动化执行记录列表 |
| `/automation/execution/detail`    | GET  | 自动化执行详情   |
| `/automation/execution/case/list` | GET  | 自动化执行明细列表 |

> 以下接口为 Jenkins / pytest 内部调用，前端无需接入：
>
> - `/automation/execution/case/pull`
> - `/automation/execution/queued`
> - `/automation/execution/start`
> - `/automation/execution/case/result`
> - `/automation/execution/finish`
> - `/automation/execution/abort`

***

## 4. 单条自动化用例执行

### 接口

- 方法：`POST`
- 路径：`/it/api/automation/case/run`

### 请求体

```json
{
  "caseId": 1001,
  "envCode": "st",
  "runMode": 1,
  "jenkinsJobName": "pytest-auto-runner",
  "remark": "前端手动触发"
}
```

### 请求参数说明

| 字段             | 类型     | 必填 | 说明                      |
| -------------- | ------ | -- | ----------------------- |
| caseId         | number | 是  | 功能用例 ID，也是自动化桥梁 ID      |
| envCode        | string | 是  | 执行环境编码                  |
| runMode        | number | 否  | 执行模式，1串行，2并行；默认1        |
| jenkinsJobName | string | 否  | 指定 Jenkins Job，不传走后端默认值 |
| remark         | string | 否  | 触发备注                    |

### 成功返回示例

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "id": 12,
    "execution_no": "AE20250920153000123",
    "trigger_type": 1,
    "project_id": 3,
    "plan_id": null,
    "plan_round_no": null,
    "source_case_id": 1001,
    "env_code": "st",
    "run_mode": 1,
    "status": 2,
    "jenkins_job_name": "pytest-auto-runner",
    "jenkins_queue_id": 321,
    "jenkins_build_number": null,
    "jenkins_build_url": null,
    "console_url": null,
    "report_url": null,
    "total_count": 1,
    "pending_count": 1,
    "running_count": 0,
    "passed_count": 0,
    "failed_count": 0,
    "blocked_count": 0,
    "skipped_count": 0,
    "not_found_count": 0,
    "trigger_by": 8,
    "trigger_source": "platform",
    "trigger_message": "http://jenkins/queue/item/321/",
    "start_time": null,
    "end_time": null,
    "duration_seconds": null,
    "ext": {},
    "created_time": "2025-09-20 15:30:00",
    "updated_time": "2025-09-20 15:30:01"
  }
}
```

### 失败返回示例

```json
{
  "code": 40009,
  "msg": "caseId、envCode 为必传参数",
  "data": null
}
```

```json
{
  "code": 40009,
  "msg": "该用例不存在或未接入自动化",
  "data": null
}
```

***

## 5. 计划自动化用例执行

### 接口

- 方法：`POST`
- 路径：`/it/api/automation/plan/run`

### 请求体：执行计划下全部自动化用例

```json
{
  "planId": 2001,
  "envCode": "st",
  "runMode": 1,
  "roundNo": 1,
  "jenkinsJobName": "pytest-auto-runner",
  "remark": "执行计划自动化"
}
```

### 请求体：执行计划下指定用例

```json
{
  "planId": 2001,
  "envCode": "st",
  "runMode": 1,
  "roundNo": 1,
  "caseIds": [1001, 1002, 1003],
  "jenkinsJobName": "pytest-auto-runner",
  "remark": "只执行勾选用例"
}
```

### 请求参数说明

| 字段             | 类型        | 必填 | 说明                              |
| -------------- | --------- | -- | ------------------------------- |
| planId         | number    | 是  | 测试计划 ID                         |
| envCode        | string    | 是  | 执行环境编码                          |
| runMode        | number    | 否  | 执行模式，1串行，2并行；默认1                |
| roundNo        | number    | 否  | 指定计划轮次                          |
| caseIds        | number\[] | 否  | 指定执行的功能用例 ID 列表；不传则执行计划下全部自动化用例 |
| jenkinsJobName | string    | 否  | 指定 Jenkins Job                  |
| remark         | string    | 否  | 触发备注                            |

### 成功返回示例

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "id": 13,
    "execution_no": "AE20250920153500123",
    "trigger_type": 2,
    "project_id": 3,
    "plan_id": 2001,
    "plan_round_no": 1,
    "source_case_id": null,
    "env_code": "st",
    "run_mode": 1,
    "status": 2,
    "jenkins_job_name": "pytest-auto-runner",
    "jenkins_queue_id": 322,
    "total_count": 10,
    "pending_count": 10,
    "running_count": 0,
    "passed_count": 0,
    "failed_count": 0,
    "blocked_count": 0,
    "skipped_count": 0,
    "not_found_count": 0
  }
}
```

### 失败返回示例

```json
{
  "code": 40009,
  "msg": "planId、envCode 为必传参数",
  "data": null
}
```

```json
{
  "code": 40009,
  "msg": "计划下无可执行自动化用例",
  "data": null
}
```

***

## 6. 自动化执行记录列表

### 接口

- 方法：`GET`
- 路径：`/it/api/automation/execution/list`

### Query 参数

| 字段          | 类型     | 必填 | 说明              |
| ----------- | ------ | -- | --------------- |
| pageNo      | number | 否  | 页码，默认1          |
| pageSize    | number | 否  | 每页数量，默认20       |
| projectId   | number | 否  | 按项目过滤           |
| planId      | number | 否  | 按计划过滤           |
| status      | number | 否  | 按执行主单状态过滤       |
| triggerType | number | 否  | 按触发类型过滤，1单条，2计划 |

### 请求示例

```http
GET /it/api/automation/execution/list?pageNo=1&pageSize=20&planId=2001
```

### 成功返回示例

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "list": [
      {
        "id": 13,
        "execution_no": "AE20250920153500123",
        "trigger_type": 2,
        "project_id": 3,
        "plan_id": 2001,
        "plan_round_no": 1,
        "source_case_id": null,
        "env_code": "st",
        "run_mode": 1,
        "status": 3,
        "jenkins_job_name": "pytest-auto-runner",
        "jenkins_queue_id": 322,
        "jenkins_build_number": 108,
        "jenkins_build_url": "http://jenkins/job/pytest-auto-runner/108/",
        "console_url": "http://jenkins/job/pytest-auto-runner/108/console",
        "report_url": "http://allure/report/108",
        "total_count": 10,
        "pending_count": 3,
        "running_count": 2,
        "passed_count": 4,
        "failed_count": 1,
        "blocked_count": 0,
        "skipped_count": 0,
        "not_found_count": 0,
        "trigger_by": 8,
        "trigger_source": "platform",
        "trigger_message": "",
        "start_time": "2025-09-20 15:36:00",
        "end_time": null,
        "duration_seconds": null,
        "ext": {},
        "created_time": "2025-09-20 15:35:00",
        "updated_time": "2025-09-20 15:38:20"
      }
    ],
    "total": 1
  }
}
```

***

## 7. 自动化执行详情

### 接口

- 方法：`GET`
- 路径：`/it/api/automation/execution/detail`

### Query 参数

| 字段          | 类型     | 必填 | 说明      |
| ----------- | ------ | -- | ------- |
| executionId | number | 是  | 执行主单 ID |

### 请求示例

```http
GET /it/api/automation/execution/detail?executionId=13
```

### 成功返回示例

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "id": 13,
    "execution_no": "AE20250920153500123",
    "trigger_type": 2,
    "project_id": 3,
    "plan_id": 2001,
    "plan_round_no": 1,
    "source_case_id": null,
    "env_code": "st",
    "run_mode": 1,
    "status": 4,
    "jenkins_job_name": "pytest-auto-runner",
    "jenkins_queue_id": 322,
    "jenkins_build_number": 108,
    "jenkins_build_url": "http://jenkins/job/pytest-auto-runner/108/",
    "console_url": "http://jenkins/job/pytest-auto-runner/108/console",
    "report_url": "http://allure/report/108",
    "total_count": 10,
    "pending_count": 0,
    "running_count": 0,
    "passed_count": 9,
    "failed_count": 1,
    "blocked_count": 0,
    "skipped_count": 0,
    "not_found_count": 0,
    "trigger_by": 8,
    "trigger_source": "platform",
    "trigger_message": "",
    "start_time": "2025-09-20 15:36:00",
    "end_time": "2025-09-20 15:45:00",
    "duration_seconds": 540,
    "ext": {},
    "created_time": "2025-09-20 15:35:00",
    "updated_time": "2025-09-20 15:45:00",
    "summary": {
      "total": 10,
      "pending": 0,
      "running": 0,
      "passed": 9,
      "failed": 1,
      "blocked": 0,
      "skipped": 0,
      "notFound": 0,
      "canceled": 0
    }
  }
}
```

### 失败返回示例

```json
{
  "code": 40011,
  "msg": "executionId 为必传参数",
  "data": null
}
```

***

## 8. 自动化执行明细列表

### 接口

- 方法：`GET`
- 路径：`/it/api/automation/execution/case/list`

### Query 参数

| 字段          | 类型     | 必填 | 说明        |
| ----------- | ------ | -- | --------- |
| executionId | number | 是  | 执行主单 ID   |
| status      | number | 否  | 按执行明细状态过滤 |
| pageNo      | number | 否  | 页码，默认1    |
| pageSize    | number | 否  | 每页数量，默认20 |

### 请求示例

```http
GET /it/api/automation/execution/case/list?executionId=13&pageNo=1&pageSize=100
```

### 成功返回示例

```json
{
  "code": 20000,
  "msg": "success",
  "data": {
    "list": [
      {
        "id": 101,
        "execution_id": 13,
        "plan_case_id": 5001,
        "case_id": 1001,
        "case_key": "1001",
        "case_title": "订单创建成功",
        "run_order": 1,
        "status": 2,
        "pytest_nodeid": "tests/order/test_create_order.py::test_create_order",
        "result_message": "执行通过",
        "error_message": "",
        "stack_trace": "",
        "report_url": "http://allure/case/101",
        "duration_seconds": 18,
        "started_time": "2025-09-20 15:36:02",
        "finished_time": "2025-09-20 15:36:20",
        "retry_count": 0,
        "ext": {},
        "created_time": "2025-09-20 15:35:00",
        "updated_time": "2025-09-20 15:36:20"
      },
      {
        "id": 102,
        "execution_id": 13,
        "plan_case_id": 5002,
        "case_id": 1002,
        "case_key": "1002",
        "case_title": "订单取消失败提示正确",
        "run_order": 2,
        "status": 3,
        "pytest_nodeid": "tests/order/test_cancel_order.py::test_cancel_order",
        "result_message": "断言失败",
        "error_message": "AssertionError: xxx",
        "stack_trace": "Traceback ...",
        "report_url": "http://allure/case/102",
        "duration_seconds": 12,
        "started_time": "2025-09-20 15:36:21",
        "finished_time": "2025-09-20 15:36:33",
        "retry_count": 0,
        "ext": {},
        "created_time": "2025-09-20 15:35:00",
        "updated_time": "2025-09-20 15:36:33"
      }
    ],
    "total": 10
  }
}
```

### 失败返回示例

```json
{
  "code": 40011,
  "msg": "executionId 为必传参数",
  "data": null
}
```

***

## 9. 前端接入建议

### 9.1 单条执行

- 页面位置：功能用例列表页 / 详情页
- 按钮：`执行自动化`
- 调用接口：`POST /automation/case/run`
- 成功后拿返回 `data.id` 作为 `executionId`
- 再调用：
  - `GET /automation/execution/detail`
  - `GET /automation/execution/case/list`

### 9.2 计划执行

- 页面位置：测试计划详情页
- 按钮：`执行自动化用例`
- 调用接口：`POST /automation/plan/run`
- 支持：
  - 执行全部自动化用例
  - 执行勾选用例（传 `caseIds`）

### 9.3 轮询建议

执行为异步触发，前端建议轮询：

- `GET /automation/execution/detail?executionId=xx`
- `GET /automation/execution/case/list?executionId=xx&pageNo=1&pageSize=100`

轮询频率建议：

- 执行中：每 3\~5 秒 1 次
- 终态停止轮询

主单终态：

- `4 成功`
- `5 失败`
- `6 已取消`
- `7 触发失败`
- `8 回调异常`

***

## 10. 备注

1. 返回字段命名为下划线风格，如：
   - `execution_no`
   - `project_id`
   - `created_time`
2. `summary` 仅在执行详情接口返回：
   - `/automation/execution/detail`
3. `report_url`、`console_url` 在刚触发时可能为空，待 Jenkins / pytest 回调后更新。

