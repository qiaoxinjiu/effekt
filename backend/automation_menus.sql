-- ==============================================
-- 自动化执行模块 - 权限对应的按钮菜单
-- ==============================================

-- 自动化执行 按钮
INSERT INTO menu (name, code, type, path, component, icon, permission_code, parent_id, sort, visible, status, is_delete)
SELECT '自动化执行', 'automation_run', 3, '', '', '', 'automation:run',
       (SELECT id FROM menu WHERE code = 'automation_list'), 1, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'automation_run');

-- 自动化执行详情 按钮
INSERT INTO menu (name, code, type, path, component, icon, permission_code, parent_id, sort, visible, status, is_delete)
SELECT '自动化执行详情', 'automation_detail', 3, '', '', '', 'automation:detail',
       (SELECT id FROM menu WHERE code = 'automation_list'), 2, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'automation_detail');

-- 自动化执行明细 按钮
INSERT INTO menu (name, code, type, path, component, icon, permission_code, parent_id, sort, visible, status, is_delete)
SELECT '自动化执行明细', 'automation_case_list', 3, '', '', '', 'automation:case_list',
       (SELECT id FROM menu WHERE code = 'automation_list'), 3, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'automation_case_list');

-- 用例拉取 按钮
INSERT INTO menu (name, code, type, path, component, icon, permission_code, parent_id, sort, visible, status, is_delete)
SELECT '用例拉取', 'automation_pull', 3, '', '', '', 'automation:pull',
       (SELECT id FROM menu WHERE code = 'automation_list'), 4, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'automation_pull');

-- 执行排队 按钮
INSERT INTO menu (name, code, type, path, component, icon, permission_code, parent_id, sort, visible, status, is_delete)
SELECT '执行排队', 'automation_queued', 3, '', '', '', 'automation:queued',
       (SELECT id FROM menu WHERE code = 'automation_list'), 5, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'automation_queued');

-- 执行开始 按钮
INSERT INTO menu (name, code, type, path, component, icon, permission_code, parent_id, sort, visible, status, is_delete)
SELECT '执行开始', 'automation_start', 3, '', '', '', 'automation:start',
       (SELECT id FROM menu WHERE code = 'automation_list'), 6, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'automation_start');

-- 用例结果 按钮
INSERT INTO menu (name, code, type, path, component, icon, permission_code, parent_id, sort, visible, status, is_delete)
SELECT '用例结果', 'automation_result', 3, '', '', '', 'automation:result',
       (SELECT id FROM menu WHERE code = 'automation_list'), 7, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'automation_result');

-- 执行完成 按钮
INSERT INTO menu (name, code, type, path, component, icon, permission_code, parent_id, sort, visible, status, is_delete)
SELECT '执行完成', 'automation_finish', 3, '', '', '', 'automation:finish',
       (SELECT id FROM menu WHERE code = 'automation_list'), 8, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'automation_finish');

-- 取消执行 按钮
INSERT INTO menu (name, code, type, path, component, icon, permission_code, parent_id, sort, visible, status, is_delete)
SELECT '取消执行', 'automation_abort', 3, '', '', '', 'automation:abort',
       (SELECT id FROM menu WHERE code = 'automation_list'), 9, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'automation_abort');

COMMIT;