-- RBAC / 用户 / 菜单 管理建表与初始化 SQL
-- PostgreSQL

BEGIN;

CREATE TABLE IF NOT EXISTS "user" (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    real_name VARCHAR(64),
    password_hash VARCHAR(255) NOT NULL,
    mobile VARCHAR(32),
    email VARCHAR(128),
    avatar VARCHAR(255),
    status SMALLINT DEFAULT 1,
    last_login_time TIMESTAMP NULL,
    created_by BIGINT,
    is_delete INTEGER DEFAULT 0,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_status ON "user" (status);
CREATE INDEX IF NOT EXISTS idx_user_is_delete ON "user" (is_delete);

CREATE TABLE IF NOT EXISTS role (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(64) NOT NULL UNIQUE,
    name VARCHAR(64) NOT NULL,
    description TEXT,
    status SMALLINT DEFAULT 1,
    is_system SMALLINT DEFAULT 0,
    created_by BIGINT,
    is_delete INTEGER DEFAULT 0,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_role_status ON role (status);
CREATE INDEX IF NOT EXISTS idx_role_is_delete ON role (is_delete);

CREATE TABLE IF NOT EXISTS permission (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(128) NOT NULL UNIQUE,
    name VARCHAR(128) NOT NULL,
    module VARCHAR(64),
    action VARCHAR(64),
    description TEXT,
    status SMALLINT DEFAULT 1,
    is_delete INTEGER DEFAULT 0,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_permission_module ON permission (module);
CREATE INDEX IF NOT EXISTS idx_permission_status ON permission (status);

CREATE TABLE IF NOT EXISTS menu (
    id BIGSERIAL PRIMARY KEY,
    parent_id BIGINT DEFAULT 0,
    name VARCHAR(64) NOT NULL,
    code VARCHAR(64) UNIQUE,
    type SMALLINT DEFAULT 1,
    path VARCHAR(255),
    component VARCHAR(255),
    icon VARCHAR(64),
    permission_code VARCHAR(128),
    sort INTEGER DEFAULT 0,
    visible SMALLINT DEFAULT 1,
    status SMALLINT DEFAULT 1,
    is_delete INTEGER DEFAULT 0,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_menu_parent_id ON menu (parent_id);
CREATE INDEX IF NOT EXISTS idx_menu_sort ON menu (sort);

CREATE TABLE IF NOT EXISTS user_role (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    is_delete INTEGER DEFAULT 0,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_user_role UNIQUE (user_id, role_id)
);

CREATE INDEX IF NOT EXISTS idx_user_role_user_id ON user_role (user_id);
CREATE INDEX IF NOT EXISTS idx_user_role_role_id ON user_role (role_id);

CREATE TABLE IF NOT EXISTS role_permission (
    id BIGSERIAL PRIMARY KEY,
    role_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,
    is_delete INTEGER DEFAULT 0,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_role_permission UNIQUE (role_id, permission_id)
);

CREATE INDEX IF NOT EXISTS idx_role_permission_role_id ON role_permission (role_id);
CREATE INDEX IF NOT EXISTS idx_role_permission_permission_id ON role_permission (permission_id);

CREATE TABLE IF NOT EXISTS role_menu (
    id BIGSERIAL PRIMARY KEY,
    role_id BIGINT NOT NULL,
    menu_id BIGINT NOT NULL,
    is_delete INTEGER DEFAULT 0,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_role_menu UNIQUE (role_id, menu_id)
);

CREATE INDEX IF NOT EXISTS idx_role_menu_role_id ON role_menu (role_id);
CREATE INDEX IF NOT EXISTS idx_role_menu_menu_id ON role_menu (menu_id);

INSERT INTO role (code, name, description, status, is_system, created_by, is_delete)
SELECT 'admin', '超级管理员', '系统内置超级管理员', 1, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM role WHERE code = 'admin');

INSERT INTO role (code, name, description, status, is_system, created_by, is_delete)
SELECT 'test_manager', '测试经理', '系统内置测试经理角色', 1, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM role WHERE code = 'test_manager');

INSERT INTO role (code, name, description, status, is_system, created_by, is_delete)
SELECT 'test_engineer', '测试工程师', '系统内置测试工程师角色', 1, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM role WHERE code = 'test_engineer');

INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'role:list', '角色列表', 'role', 'list', '查看角色列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'role:create', '创建角色', 'role', 'create', '创建角色', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'role:update', '更新角色', 'role', 'update', '更新角色', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role:update');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'role:delete', '删除角色', 'role', 'delete', '删除角色', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role:delete');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'user:list', '用户列表', 'user', 'list', '查看用户列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'user:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'user:create', '创建用户', 'user', 'create', '创建用户', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'user:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'user:update', '更新用户', 'user', 'update', '更新用户', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'user:update');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'user:delete', '删除用户', 'user', 'delete', '删除用户', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'user:delete');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'permission:list', '权限列表', 'permission', 'list', '查看权限列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'permission:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'menu:list', '菜单列表', 'menu', 'list', '查看菜单树', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'menu:list');

INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'role:detail', '角色详情', 'role', 'detail', '查看角色详情', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role:detail');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'permission:detail', '权限详情', 'permission', 'detail', '查看权限详情', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'permission:detail');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'permission:create', '创建权限', 'permission', 'create', '创建权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'permission:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'permission:update', '更新权限', 'permission', 'update', '更新权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'permission:update');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'permission:delete', '删除权限', 'permission', 'delete', '删除权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'permission:delete');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'menu:detail', '菜单详情', 'menu', 'detail', '查看菜单详情', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'menu:detail');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'menu:create', '创建菜单', 'menu', 'create', '创建菜单', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'menu:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'menu:update', '更新菜单', 'menu', 'update', '更新菜单', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'menu:update');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'menu:delete', '删除菜单', 'menu', 'delete', '删除菜单', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'menu:delete');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'user:detail', '用户详情', 'user', 'detail', '查看用户详情', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'user:detail');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'project:list', '项目列表', 'project', 'list', '查看项目列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'project:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'project:detail', '项目详情', 'project', 'detail', '查看项目详情', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'project:detail');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'project:create', '创建项目', 'project', 'create', '创建项目', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'project:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'project:update', '更新项目', 'project', 'update', '更新项目', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'project:update');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'project:delete', '删除项目', 'project', 'delete', '删除项目', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'project:delete');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'project_member:list', '项目成员列表', 'project_member', 'list', '查看项目成员列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'project_member:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'project_member:create', '创建项目成员', 'project_member', 'create', '创建项目成员', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'project_member:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'product:list', '产品列表', 'product', 'list', '查看产品列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'product:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'product:detail', '产品详情', 'product', 'detail', '查看产品详情', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'product:detail');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'product:create', '创建产品', 'product', 'create', '创建产品', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'product:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'product:update', '更新产品', 'product', 'update', '更新产品', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'product:update');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'product:delete', '删除产品', 'product', 'delete', '删除产品', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'product:delete');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'module:list', '模块列表', 'module', 'list', '查看模块列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'module:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'module:create', '创建模块', 'module', 'create', '创建模块', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'module:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'module:update', '更新模块', 'module', 'update', '更新模块', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'module:update');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'module:delete', '删除模块', 'module', 'delete', '删除模块', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'module:delete');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'case:list', '用例列表', 'case', 'list', '查看用例列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'case:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'case:detail', '用例详情', 'case', 'detail', '查看用例详情', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'case:detail');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'case:create', '创建用例', 'case', 'create', '创建用例', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'case:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'case:update', '更新用例', 'case', 'update', '更新用例', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'case:update');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'case:delete', '删除用例', 'case', 'delete', '删除用例', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'case:delete');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'case_snapshot:create', '创建用例快照', 'case_snapshot', 'create', '创建用例快照', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'case_snapshot:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'case_snapshot:list', '用例快照列表', 'case_snapshot', 'list', '查看用例快照列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'case_snapshot:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'case_review:create', '创建用例评审', 'case_review', 'create', '创建用例评审', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'case_review:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'case_review:update', '更新用例评审', 'case_review', 'update', '更新用例评审', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'case_review:update');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'case_review:list', '用例评审列表', 'case_review', 'list', '查看用例评审列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'case_review:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan:list', '计划列表', 'plan', 'list', '查看计划列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan:detail', '计划详情', 'plan', 'detail', '查看计划详情', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan:detail');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan:create', '创建计划', 'plan', 'create', '创建计划', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan:update', '更新计划', 'plan', 'update', '更新计划', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan:update');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan:delete', '删除计划', 'plan', 'delete', '删除计划', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan:delete');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan:progress', '计划进度', 'plan', 'progress', '查看计划进度', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan:progress');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan_round:create', '创建计划轮次', 'plan_round', 'create', '创建计划轮次', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan_round:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan_round:list', '计划轮次列表', 'plan_round', 'list', '查看计划轮次列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan_round:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan_case:add', '添加计划用例', 'plan_case', 'add', '添加计划用例', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan_case:add');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan_case:list', '计划用例列表', 'plan_case', 'list', '查看计划用例列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan_case:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan_case:execute', '执行计划用例', 'plan_case', 'execute', '执行计划用例', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan_case:execute');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'report:list', '报告列表', 'report', 'list', '查看报告列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'report:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'report:detail', '报告详情', 'report', 'detail', '查看报告详情', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'report:detail');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'report:generate', '生成报告', 'report', 'generate', '生成报告', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'report:generate');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'data_builder:list', '造数器列表', 'data_builder', 'list', '查看造数器列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'data_builder:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'sql_project:list', 'SQL项目列表', 'sql_project', 'list', '查看SQL项目列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'sql_project:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'sql_project:create', '创建SQL项目', 'sql_project', 'create', '创建SQL项目', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'sql_project:create');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'sql_project:detail', 'SQL项目详情', 'sql_project', 'detail', '查看SQL项目详情', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'sql_project:detail');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'sql_project:delete', '删除SQL项目', 'sql_project', 'delete', '删除SQL项目', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'sql_project:delete');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'sql_project:execute', '执行SQL项目', 'sql_project', 'execute', '执行SQL项目', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'sql_project:execute');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'role_permission:list', '角色权限列表', 'role_permission', 'list', '查看角色权限列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role_permission:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'role_permission:assign', '分配角色权限', 'role_permission', 'assign', '分配角色权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role_permission:assign');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'role_menu:list', '角色菜单列表', 'role_menu', 'list', '查看角色菜单列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role_menu:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'role_menu:assign', '分配角色菜单', 'role_menu', 'assign', '分配角色菜单', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role_menu:assign');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'user_role:list', '用户角色列表', 'user_role', 'list', '查看用户角色列表', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'user_role:list');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'user_role:assign', '分配用户角色', 'user_role', 'assign', '分配用户角色', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'user_role:assign');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'role:*', '角色全部权限', 'role', '*', '角色模块全部权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'role:*');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'user:*', '用户全部权限', 'user', '*', '用户模块全部权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'user:*');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'menu:*', '菜单全部权限', 'menu', '*', '菜单模块全部权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'menu:*');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'permission:*', '权限全部权限', 'permission', '*', '权限模块全部权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'permission:*');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'project:*', '项目全部权限', 'project', '*', '项目模块全部权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'project:*');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'environment:*', '环境全部权限', 'environment', '*', '环境模块全部权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'environment:*');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'case:*', '用例全部权限', 'case', '*', '用例模块全部权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'case:*');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'plan:*', '计划全部权限', 'plan', '*', '计划模块全部权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'plan:*');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'report:*', '报告全部权限', 'report', '*', '报告模块全部权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'report:*');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT 'data_builder:*', '造数器全部权限', 'data_builder', '*', '造数器模块全部权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = 'data_builder:*');
INSERT INTO permission (code, name, module, action, description, status, is_delete)
SELECT '*:*', '全部权限', '*', '*', '所有模块全部权限', 1, 0
WHERE NOT EXISTS (SELECT 1 FROM permission WHERE code = '*:*');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT 0, '系统管理', 'system', 1, '/system', 'Layout', 'setting', NULL, 1, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'system');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT m.id, '角色管理', 'role_manage', 2, '/system/role', 'system/role/index', 'peoples', 'role:list', 1, 1, 1, 0
FROM menu m
WHERE m.code = 'system'
  AND NOT EXISTS (SELECT 1 FROM menu WHERE code = 'role_manage');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT m.id, '用户管理', 'user_manage', 2, '/system/user', 'system/user/index', 'user', 'user:list', 2, 1, 1, 0
FROM menu m
WHERE m.code = 'system'
  AND NOT EXISTS (SELECT 1 FROM menu WHERE code = 'user_manage');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT m.id, '权限管理', 'permission_manage', 2, '/system/permission', 'system/permission/index', 'lock', 'permission:list', 3, 1, 1, 0
FROM menu m
WHERE m.code = 'system'
  AND NOT EXISTS (SELECT 1 FROM menu WHERE code = 'permission_manage');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT m.id, '菜单管理', 'menu_manage', 2, '/system/menu', 'system/menu/index', 'menu', 'menu:list', 4, 1, 1, 0
FROM menu m
WHERE m.code = 'system'
  AND NOT EXISTS (SELECT 1 FROM menu WHERE code = 'menu_manage');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT 0, '测试平台', 'test_platform', 1, '/test-platform', 'Layout', 'platform', NULL, 2, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'test_platform');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT m.id, '产品管理', 'product_manage', 2, '/test-platform/product', 'test-platform/product/index', 'product', 'product:list', 1, 1, 1, 0
FROM menu m
WHERE m.code = 'test_platform'
  AND NOT EXISTS (SELECT 1 FROM menu WHERE code = 'product_manage');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT m.id, '项目管理', 'project_manage', 2, '/test-platform/project', 'test-platform/project/index', 'project', 'project:list', 2, 1, 1, 0
FROM menu m
WHERE m.code = 'test_platform'
  AND NOT EXISTS (SELECT 1 FROM menu WHERE code = 'project_manage');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT m.id, '用例管理', 'case_manage', 2, '/test-platform/case', 'test-platform/case/index', 'case', 'case:list', 3, 1, 1, 0
FROM menu m
WHERE m.code = 'test_platform'
  AND NOT EXISTS (SELECT 1 FROM menu WHERE code = 'case_manage');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT m.id, '测试计划', 'plan_manage', 2, '/test-platform/plan', 'test-platform/plan/index', 'plan', 'plan:list', 4, 1, 1, 0
FROM menu m
WHERE m.code = 'test_platform'
  AND NOT EXISTS (SELECT 1 FROM menu WHERE code = 'plan_manage');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT m.id, '测试报告', 'report_manage', 2, '/test-platform/report', 'test-platform/report/index', 'report', 'report:list', 5, 1, 1, 0
FROM menu m
WHERE m.code = 'test_platform'
  AND NOT EXISTS (SELECT 1 FROM menu WHERE code = 'report_manage');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT 0, '造数工具', 'data_tools', 1, '/data-tools', 'Layout', 'data', NULL, 3, 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM menu WHERE code = 'data_tools');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT m.id, '数据库造数', 'data_builder_manage', 2, '/data-tools/db-builder', 'data-tools/db-builder/index', 'database', 'data_builder:list', 1, 1, 1, 0
FROM menu m
WHERE m.code = 'data_tools'
  AND NOT EXISTS (SELECT 1 FROM menu WHERE code = 'data_builder_manage');

INSERT INTO menu (parent_id, name, code, type, path, component, icon, permission_code, sort, visible, status, is_delete)
SELECT m.id, '造数工厂', 'data_factory_manage', 2, '/data-tools/factory', 'data-tools/factory/index', 'factory', NULL, 2, 1, 1, 0
FROM menu m
WHERE m.code = 'data_tools'
  AND NOT EXISTS (SELECT 1 FROM menu WHERE code = 'data_factory_manage');

INSERT INTO "user" (username, real_name, password_hash, mobile, email, avatar, status, created_by, is_delete)
SELECT 'admin', '系统管理员', 'admin123', '13800000000', 'admin@example.com', '', 1, 1, 0
WHERE NOT EXISTS (SELECT 1 FROM "user" WHERE username = 'admin');

INSERT INTO user_role (user_id, role_id, is_delete)
SELECT u.id, r.id, 0
FROM "user" u, role r
WHERE u.username = 'admin' AND r.code = 'admin'
  AND NOT EXISTS (
      SELECT 1 FROM user_role ur WHERE ur.user_id = u.id AND ur.role_id = r.id
  );

INSERT INTO role_permission (role_id, permission_id, is_delete)
SELECT r.id, p.id, 0
FROM role r, permission p
WHERE r.code = 'admin'
  AND NOT EXISTS (
      SELECT 1 FROM role_permission rp WHERE rp.role_id = r.id AND rp.permission_id = p.id
  );

INSERT INTO role_permission (role_id, permission_id, is_delete)
SELECT r.id, p.id, 0
FROM role r, permission p
WHERE r.code = 'admin'
  AND p.code IN ('user_role:list', 'user_role:assign', 'role_permission:list', 'role_permission:assign', 'role_menu:list', 'role_menu:assign')
  AND NOT EXISTS (
      SELECT 1 FROM role_permission rp WHERE rp.role_id = r.id AND rp.permission_id = p.id
  );

UPDATE menu SET permission_code = 'role:list' WHERE code = 'role_manage' AND (permission_code IS NULL OR permission_code = '');
UPDATE menu SET permission_code = 'user:list' WHERE code = 'user_manage' AND (permission_code IS NULL OR permission_code = '');
UPDATE menu SET permission_code = 'permission:list' WHERE code = 'permission_manage' AND (permission_code IS NULL OR permission_code = '');
UPDATE menu SET permission_code = 'menu:list' WHERE code = 'menu_manage' AND (permission_code IS NULL OR permission_code = '');
UPDATE menu SET permission_code = 'product:list' WHERE code = 'product_manage' AND (permission_code IS NULL OR permission_code = '');
UPDATE menu SET permission_code = 'project:list' WHERE code = 'project_manage' AND (permission_code IS NULL OR permission_code = '');
UPDATE menu SET permission_code = 'case:list' WHERE code = 'case_manage' AND (permission_code IS NULL OR permission_code = '');
UPDATE menu SET permission_code = 'plan:list' WHERE code = 'plan_manage' AND (permission_code IS NULL OR permission_code = '');
UPDATE menu SET permission_code = 'report:list' WHERE code = 'report_manage' AND (permission_code IS NULL OR permission_code = '');
UPDATE menu SET permission_code = 'data_builder:list' WHERE code = 'data_builder_manage' AND (permission_code IS NULL OR permission_code = '');

INSERT INTO role_menu (role_id, menu_id, is_delete)
SELECT r.id, m.id, 0
FROM role r, menu m
WHERE r.code = 'admin'
  AND NOT EXISTS (
      SELECT 1 FROM role_menu rm WHERE rm.role_id = r.id AND rm.menu_id = m.id
  );

COMMIT;
