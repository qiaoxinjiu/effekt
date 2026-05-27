# 执行计划：用例管理与模块管理改造

## 目标
根据后端 `Case 与 Module` 接口文档，改造前端接口调用与用例管理页面：
- 用例管理页面包含两个表格：模块列表、用例列表。
- 模块支持查询、新增、删除，并展示模块字段与搜索条件。
- 用例列表支持项目名称、用例标题模糊搜索、优先级、是否自动化、标签等条件。
- 用例列表展示项目名称、用例编号、用例标题、优先级、类型、状态、是否实现自动化、标签等字段。

## 已定位文件
- `src/api/caseApi.js`
  - 已有 `module/tree/create/update/delete` 与 `case/list/detail/create/update/delete` 封装。
  - 当前部分参数仍使用旧字段：`project_id`、`case_id` 等，需要调整为文档里的 camelCase 参数。
- `src/components/TestPlatform/Case/CaseList.vue`
  - 当前只有一个用例表格。
  - 当前搜索条件只有项目ID、关键词、优先级。
  - 当前缺少分页状态定义与模块管理区。
- `src/components/TestPlatform/Case/CaseEditor.vue`
  - 当前表单字段使用 `case_type` 等后端返回字段，提交时需要按文档转为 `caseType`、`moduleId`、`caseKey`、`isAuto` 等。
- `src/router/index.js`
  - 用例相关路由已存在，无需新增路由。

## 改造步骤

### 1. 调整接口封装 `src/api/caseApi.js`
- 保留已有函数名，降低页面调用改动成本。
- `getCaseList(projectId, params)` 改为请求参数包含：
  - `projectId`
  - `pageNo`
  - `pageSize`
  - `projectName`
  - `moduleId`
  - `keyword`
  - `priority`
  - `caseType`
  - `status`
  - `isAuto`
  - `tag`
- `getCaseDetail(projectId, caseId)` 改为传 `caseId`，必要时兼容 `projectId`。
- `createCase(projectId, data)` 改为提交 `projectId`，不再提交 `project_id`。
- `updateCase(projectId, caseId, data)` 改为提交 `caseId`，不再提交 `id/project_id` 旧字段。
- `deleteCase(projectId, caseId)` 改为提交 `{ caseId }`，必要时保留 `projectId` 不影响后端。
- 模块接口保持：
  - `getModuleTree(params)` -> `/module/tree`
  - `createModule(data)` -> `/module/create`
  - `deleteModule(data)` -> `/module/delete`
  - 删除模块调用传 `{ moduleId }`。

### 2. 改造 `CaseList.vue` 页面布局
- 在同一个页面内使用两个 `page-section`：
  1. `模块列表`
  2. `用例列表`
- 模块列表区：
  - 搜索条件：`projectId`、`parentId`。
  - 按钮：查询、新增模块。
  - 表格字段：
    - 模块ID：`id`
    - 项目ID：`project_id`
    - 父模块ID：`parent_id`
    - 模块名称：`name`
    - 排序：`sort_order`
    - 路径：`path`
    - 创建时间：`created_time`
    - 更新时间：`updated_time`
    - 操作：删除
  - 新增模块弹窗字段：
    - `projectId` 必填
    - `name` 必填
    - `parentId`
    - `sortOrder`
    - `path`
  - 删除模块调用 `deleteModule({ moduleId: row.id })`。

### 3. 改造用例列表搜索条件
- 搜索表单字段：
  - `projectId`
  - `projectName`
  - `keyword`（用例标题模糊搜索）
  - `priority`
  - `caseType`
  - `status`
  - `isAuto`
  - `tag`
- 查询时传入分页：`pageNo`、`pageSize`。
- 查询成功后兼容读取：`data.list || data.items || []`，`data.total || list.length`。

### 4. 改造用例列表表格字段展示
- 表格字段：
  - 项目名称：`project_name`
  - 用例编号：`case_key`
  - 用例标题：`title`
  - 优先级：`priority`，格式化为 `P0/P1/P2/P3`
  - 类型：`case_type`，格式化为 `功能/性能/安全/接口`
  - 状态：`status`，格式化为 `正常/已废弃/评审中`
  - 是否实现自动化：`is_auto`，格式化为 `已实现/未实现`
  - 标签：`tags`，数组使用 `el-tag` 展示，字符串兜底直接展示
  - 操作：编辑、评审、删除
- 删除用例调用 `deleteCase(projectId, row.id)`。

### 5. 补齐分页与交互逻辑
- `CaseList.vue` 增加：
  - `pageNo`
  - `pageSize`
  - `total`
  - `moduleLoading`
  - `moduleData`
  - `moduleQueryForm`
  - `moduleDialogVisible`
  - `moduleSubmitting`
  - `moduleForm`
  - `moduleRules`
- 增加方法：
  - `fetchModuleList`
  - `openModuleCreate`
  - `resetModuleForm`
  - `submitModuleCreate`
  - `removeModule`
  - `handleSizeChange`
  - `handleCurrentChange`
  - `formatPriority`
  - `formatCaseType`
  - `formatStatus`
  - `formatIsAuto`
  - `formatTags`

### 6. 调整 `CaseEditor.vue` 提交字段
- 详情加载：兼容后端 snake_case 返回字段，映射到表单：
  - `module_id` -> `moduleId`
  - `case_key` -> `caseKey`
  - `case_type` -> `caseType`
  - `is_auto` -> `isAuto`
- 表单补充字段：
  - 模块ID
  - 用例编号
  - 状态
  - 是否自动化
- 保存前构造 payload：
  - `projectId`
  - `moduleId`
  - `caseKey`
  - `title`
  - `preconditions`
  - `steps`
  - `priority`
  - `caseType`
  - `tags`
  - `status`
  - `isAuto`
- 新增调用 `createCase(projectId, payload)`。
- 编辑调用 `updateCase(projectId, caseId, payload)`。

### 7. 验证
- 优先运行：`npm run build`。
- 如构建耗时或环境缺依赖，至少做静态检查：确认 Vue 模板字段、方法引用、导入函数均存在。

## 预期改动范围
- 修改：`src/api/caseApi.js`
- 修改：`src/components/TestPlatform/Case/CaseList.vue`
- 修改：`src/components/TestPlatform/Case/CaseEditor.vue`
- 不新增路由，不新增依赖。

## 风险与兼容处理
- 后端返回字段是 snake_case，前端提交字段是 camelCase，需要在编辑页做映射。
- 若后端仍兼容旧字段，当前改造会优先使用新文档字段；删除/详情可保留少量兼容参数但不依赖旧字段。
- 模块树接口可能返回树形结构，但当前需求是模块列表 table；表格直接展示返回 list，不做树形展开，除非后续明确需要树表。