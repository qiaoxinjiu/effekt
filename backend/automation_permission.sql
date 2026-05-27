-- ==============================================
-- 自动化执行模块 - menu 表插入语句
-- ==============================================

-- 自动化执行菜单（一级菜单）
INSERT INTO menu (name, code, type, path, component, icon, permission_code, parent_id, sort, visible, status, is_delete)
SELECT '自动化执行', 'automation', 1, '/automation', 'automation/index', 'auto', 'automation:*', 0, 10, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'automation');

-- 自动化执行记录列表（二级菜单）
INSERT INTO menu (name, code, type, path, component, icon, permission_code, parent_id, sort, visible, status, is_delete)
SELECT '执行记录', 'automation_list', 2, '/automation/execution', 'automation/execution', 'list', 'automation:list', 
       (SELECT id FROM menu WHERE code = 'automation'), 1, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'automation_list');

-- ==============================================
-- 自动化执行模块 - permission 表插入语句
-- ==============================================

-- 自动化用例执行权限
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'automation:run', '自动化执行', 'automation', 'run', '单条/计划自动化用例执行', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'automation:run');

-- 自动化执行记录列表权限
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'automation:list', '自动化执行列表', 'automation', 'list', '查看自动化执行记录列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'automation:list');

-- 自动化执行详情权限
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'automation:detail', '自动化执行详情', 'automation', 'detail', '查看自动化执行详情', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'automation:detail');

-- 自动化执行明细列表权限
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'automation:case_list', '自动化执行明细', 'automation', 'case_list', '查看自动化执行明细列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'automation:case_list');

-- Jenkins回调相关权限（内部接口，无需前端权限）
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'automation:pull', '用例拉取', 'automation', 'pull', 'Jenkins拉取待执行用例', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'automation:pull');

INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'automation:queued', '执行排队', 'automation', 'queued', 'Jenkins回调排队状态', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'automation:queued');

INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'automation:start', '执行开始', 'automation', 'start', 'Jenkins回调执行开始', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'automation:start');

INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'automation:result', '用例结果', 'automation', 'result', 'Jenkins回调用例结果', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'automation:result');

INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'automation:finish', '执行完成', 'automation', 'finish', 'Jenkins回调执行完成', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'automation:finish');

INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'automation:abort', '取消执行', 'automation', 'abort', 'Jenkins回调取消执行', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'automation:abort');

-- ==============================================
-- 更新 menu 表的 permission_code 关联
-- ==============================================

-- 更新自动化执行菜单的 permission_code
UPDATE menu 
SET permission_code = 'automation:*'
WHERE code = 'automation' AND permission_code IS NULL;

-- 更新执行记录菜单的 permission_code
UPDATE menu 
SET permission_code = 'automation:list'
WHERE code = 'automation_list' AND permission_code IS NULL;

COMMIT;

-- ==============================================
-- 权限清单汇总
-- ==============================================
-- | 权限代码              | 权限名称        | 对应接口                              |
-- |---------------------|--------------|-----------------------------------|
-- | automation:run      | 自动化执行      | POST /automation/case/run          |
-- |                     |              | POST /automation/plan/run          |
-- | automation:list     | 自动化执行列表    | GET /automation/execution/list     |
-- | automation:detail   | 自动化执行详情    | GET /automation/execution/detail   |
-- | automation:case_list| 自动化执行明细    | GET /automation/execution/case/list|
-- | automation:pull     | 用例拉取        | GET /automation/execution/case/pull|
-- | automation:queued   | 执行排队        | POST /automation/execution/queued  |
-- | automation:start    | 执行开始        | POST /automation/execution/start   |
-- | automation:result   | 用例结果        | POST /automation/execution/case/result|
-- | automation:finish   | 执行完成        | POST /automation/execution/finish  |
-- | automation:abort    | 取消执行        | POST /automation/execution/abort   |