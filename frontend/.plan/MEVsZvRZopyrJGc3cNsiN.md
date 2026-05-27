# 前端实现计划：测试平台页面与接口

## 1. 现状确认
- 当前项目不是 React 18 + TypeScript，而是 **Vue 2 + Element UI + vue-router + vuex + axios**。
- 已有页面以“效能平台/造数工具”为主，目录集中在：
  - `src/components/`
  - `src/api/`
  - `src/router/index.js`
- 已存在一套造数相关接口封装：`src/api/CreateDtapi.js`
- 已存在基础布局页：`src/components/Home.vue`
- 因此本次应遵循**现有 Vue 2 结构**落地，不直接按你给出的 React 目录硬切，否则与当前代码库不兼容。

## 2. 实施目标
按你提供的详细设计，在当前项目结构下补齐并升级前端代码，重点实现：
- 测试平台导航结构
- 项目/用例/计划/报告/造数 五大功能入口页面
- 对应 API 封装层
- 页面级列表、详情、表单、执行、报告查看等基础交互
- 复用当前 Element UI 风格，保持现有代码可运行

## 3. 实施范围拆分

### 阶段 A：基础设施与路由改造
1. 梳理现有路由与导航。
2. 扩展左侧菜单，新增模块入口：
   - 项目管理
   - 用例管理
   - 测试计划
   - 测试报告
   - 造数工厂
3. 在 `src/router/index.js` 注册对应页面路由。
4. 保留现有造数页面入口，避免破坏已有功能。

### 阶段 B：API 服务层补齐
1. 新增 API 文件，按你给出的接口定义封装：
   - `src/api/projectApi.js`
   - `src/api/caseApi.js`
   - `src/api/planApi.js`
   - `src/api/reportApi.js`
   - `src/api/dataFactoryApi.js`
2. 统一复用 `src/utils/request.js`。
3. 尽量映射到 REST 风格路径，例如：
   - `/api/v1/projects/{projectId}/case`
   - `/api/v1/projects/{projectId}/plan`
   - `/api/v1/projects/{projectId}/reports`
   - `/api/v1/projects/{projectId}/data/*`
4. 对分页、详情、创建、更新、执行、导出等接口做最小可用封装。

### 阶段 C：页面骨架实现
在 `src/components/` 下新增测试平台模块页面，优先做可运行页面骨架与核心交互：

1. 项目模块
   - `src/components/TestPlatform/Project/ProjectList.vue`
   - `src/components/TestPlatform/Project/ProjectDetail.vue`
   - `src/components/TestPlatform/Project/ProjectSettings.vue`

2. 用例模块
   - `src/components/TestPlatform/Case/CaseList.vue`
   - `src/components/TestPlatform/Case/CaseEditor.vue`
   - `src/components/TestPlatform/Case/CaseReview.vue`

3. 测试计划模块
   - `src/components/TestPlatform/Plan/PlanList.vue`
   - `src/components/TestPlatform/Plan/PlanBuilder.vue`
   - `src/components/TestPlatform/Plan/PlanExecute.vue`
   - `src/components/TestPlatform/Plan/PlanProgress.vue`

4. 报告模块
   - `src/components/TestPlatform/Report/ReportList.vue`
   - `src/components/TestPlatform/Report/ReportViewer.vue`

5. 造数模块升级
   - 保留现有 `CreateData/*`
   - 新增测试平台语义下页面：
     - `src/components/TestPlatform/DataFactory/BuilderList.vue`
     - `src/components/TestPlatform/DataFactory/BuilderEditor.vue`
     - `src/components/TestPlatform/DataFactory/TaskHistory.vue`
     - `src/components/TestPlatform/DataFactory/MockService.vue`

### 阶段 D：公共组件抽取
新增可复用基础组件，减少页面重复：
- `src/components/TestPlatform/common/JsonViewer.vue`
- `src/components/TestPlatform/common/KeyValueDescriptions.vue`
- `src/components/TestPlatform/common/PageSection.vue`

### 阶段 E：联调友好处理
1. 页面初版支持后端未完成时的容错：
   - 空数据态
   - 请求失败提示
   - 默认 projectId 占位
2. 不引入新依赖，避免额外安装。
3. 保持接口函数独立，后续联调时只需替换 URL 或参数格式。

## 4. 执行顺序
1. 先改路由与主页导航。
2. 再补 API 封装。
3. 再按模块逐步落页面：
   - 项目
   - 用例
   - 计划
   - 报告
   - 造数
4. 最后做公共组件复用与样式收口。

## 5. 每阶段交付物
- 阶段 A：可点击进入的菜单与路由
- 阶段 B：完整接口文件
- 阶段 C：各模块页面可打开、可发请求、可展示表格/表单
- 阶段 D：重复 UI 收敛
- 阶段 E：整体自检，确保不破坏原有功能

## 6. 风险与约束
- 当前代码库是旧版 Vue 2 工程，不能直接生成 React/TSX 代码。
- 你的接口设计是目标态，实际后端返回结构可能与设计不完全一致，因此前端会适当做字段兼容。
- 由于当前 `request.js` 已固定 `baseURL`，本次先复用，不额外改动接口基础配置，避免影响现有功能。

## 7. 本次建议执行策略
按“先骨架、再细化”的方式推进：
- 第一步：完成导航、路由、API 文件、页面骨架
- 第二步：优先把列表页和详情/编辑页做成可联调版本
- 第三步：再补计划执行、报告查看、造数编排等复杂交互

## 8. 下一步实际执行内容
获批后，我将从以下顺序开始落地：
1. 修改 `src/components/Home.vue` 增加测试平台菜单
2. 修改 `src/router/index.js` 注册测试平台路由
3. 新增五类 API 文件
4. 新增项目/用例/计划/报告/造数页面骨架
5. 检查并修正页面间跳转与基础请求
