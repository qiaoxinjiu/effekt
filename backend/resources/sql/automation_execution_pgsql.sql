-- 自动化执行建表脚本（PostgreSQL）
-- 说明：
-- 1. 本脚本为可直接执行脚本。
-- 2. 使用 PostgreSQL 标准 COMMENT ON 语法为表和字段添加注释。
-- 3. 当前脚本仅创建自动化执行主表、执行明细表、索引、更新时间触发器。
-- 4. 如需外键约束，请根据你当前库中的 test_plan / test_case / plan_case 实际表名补充。

BEGIN;

CREATE TABLE IF NOT EXISTS public.auto_execution (
    id BIGSERIAL PRIMARY KEY,
    execution_no VARCHAR(64) NOT NULL,
    trigger_type SMALLINT NOT NULL,
    project_id BIGINT NOT NULL,
    plan_id BIGINT NULL,
    plan_round_no INTEGER NULL,
    source_case_id BIGINT NULL,
    env_code VARCHAR(32) NOT NULL,
    run_mode SMALLINT NOT NULL DEFAULT 1,
    status SMALLINT NOT NULL DEFAULT 0,
    jenkins_job_name VARCHAR(128) NULL,
    jenkins_queue_id BIGINT NULL,
    jenkins_build_number BIGINT NULL,
    jenkins_build_url VARCHAR(512) NULL,
    console_url VARCHAR(512) NULL,
    report_url VARCHAR(512) NULL,
    total_count INTEGER NOT NULL DEFAULT 0,
    pending_count INTEGER NOT NULL DEFAULT 0,
    running_count INTEGER NOT NULL DEFAULT 0,
    passed_count INTEGER NOT NULL DEFAULT 0,
    failed_count INTEGER NOT NULL DEFAULT 0,
    blocked_count INTEGER NOT NULL DEFAULT 0,
    skipped_count INTEGER NOT NULL DEFAULT 0,
    not_found_count INTEGER NOT NULL DEFAULT 0,
    trigger_by BIGINT NULL,
    trigger_source VARCHAR(32) NOT NULL DEFAULT 'platform',
    trigger_message TEXT NULL,
    start_time TIMESTAMP NULL,
    end_time TIMESTAMP NULL,
    duration_seconds INTEGER NULL,
    callback_token VARCHAR(128) NULL,
    ext JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_auto_execution_no UNIQUE (execution_no)
);

COMMENT ON TABLE public.auto_execution IS '自动化执行主表';
COMMENT ON COLUMN public.auto_execution.id IS '主键ID';
COMMENT ON COLUMN public.auto_execution.execution_no IS '执行编号，平台生成，唯一';
COMMENT ON COLUMN public.auto_execution.trigger_type IS '触发类型：1-单条执行，2-计划执行';
COMMENT ON COLUMN public.auto_execution.project_id IS '项目ID';
COMMENT ON COLUMN public.auto_execution.plan_id IS '计划ID，单条执行时可为空';
COMMENT ON COLUMN public.auto_execution.plan_round_no IS '计划轮次快照';
COMMENT ON COLUMN public.auto_execution.source_case_id IS '单条执行时的来源功能用例 case_id';
COMMENT ON COLUMN public.auto_execution.env_code IS '执行环境编码，如 test/uat/prod-pre';
COMMENT ON COLUMN public.auto_execution.run_mode IS '执行模式：1-串行，2-并行';
COMMENT ON COLUMN public.auto_execution.status IS '执行状态：0-待触发，1-触发中，2-排队中，3-执行中，4-成功，5-失败，6-已取消，7-触发失败，8-回调异常';
COMMENT ON COLUMN public.auto_execution.jenkins_job_name IS 'Jenkins 任务名称';
COMMENT ON COLUMN public.auto_execution.jenkins_queue_id IS 'Jenkins 队列ID';
COMMENT ON COLUMN public.auto_execution.jenkins_build_number IS 'Jenkins 构建号';
COMMENT ON COLUMN public.auto_execution.jenkins_build_url IS 'Jenkins 构建地址';
COMMENT ON COLUMN public.auto_execution.console_url IS 'Jenkins 控制台地址';
COMMENT ON COLUMN public.auto_execution.report_url IS '聚合测试报告地址';
COMMENT ON COLUMN public.auto_execution.total_count IS '执行总用例数';
COMMENT ON COLUMN public.auto_execution.pending_count IS '待执行用例数';
COMMENT ON COLUMN public.auto_execution.running_count IS '执行中用例数';
COMMENT ON COLUMN public.auto_execution.passed_count IS '通过用例数';
COMMENT ON COLUMN public.auto_execution.failed_count IS '失败用例数';
COMMENT ON COLUMN public.auto_execution.blocked_count IS '阻塞用例数';
COMMENT ON COLUMN public.auto_execution.skipped_count IS '跳过用例数';
COMMENT ON COLUMN public.auto_execution.not_found_count IS '未找到自动化用例数';
COMMENT ON COLUMN public.auto_execution.trigger_by IS '触发人用户ID';
COMMENT ON COLUMN public.auto_execution.trigger_source IS '触发来源，默认 platform';
COMMENT ON COLUMN public.auto_execution.trigger_message IS '触发说明、失败原因或补充消息';
COMMENT ON COLUMN public.auto_execution.start_time IS '实际开始执行时间';
COMMENT ON COLUMN public.auto_execution.end_time IS '实际结束执行时间';
COMMENT ON COLUMN public.auto_execution.duration_seconds IS '执行耗时，单位秒';
COMMENT ON COLUMN public.auto_execution.callback_token IS '本次执行给 pytest/Jenkins 使用的拉取 token';
COMMENT ON COLUMN public.auto_execution.ext IS '扩展字段，JSONB';
COMMENT ON COLUMN public.auto_execution.created_time IS '创建时间';
COMMENT ON COLUMN public.auto_execution.updated_time IS '更新时间';

CREATE TABLE IF NOT EXISTS public.auto_execution_case (
    id BIGSERIAL PRIMARY KEY,
    execution_id BIGINT NOT NULL,
    plan_case_id BIGINT NULL,
    case_id BIGINT NOT NULL,
    case_key VARCHAR(64) NULL,
    case_title VARCHAR(255) NULL,
    run_order INTEGER NOT NULL DEFAULT 0,
    status SMALLINT NOT NULL DEFAULT 0,
    pytest_nodeid VARCHAR(512) NULL,
    result_message TEXT NULL,
    error_message TEXT NULL,
    stack_trace TEXT NULL,
    report_url VARCHAR(512) NULL,
    duration_seconds INTEGER NULL,
    started_time TIMESTAMP NULL,
    finished_time TIMESTAMP NULL,
    retry_count INTEGER NOT NULL DEFAULT 0,
    ext JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_auto_execution_case_exec_case UNIQUE (execution_id, case_id)
);

COMMENT ON TABLE public.auto_execution_case IS '自动化执行明细表';
COMMENT ON COLUMN public.auto_execution_case.id IS '主键ID';
COMMENT ON COLUMN public.auto_execution_case.execution_id IS '执行主单ID，对应 auto_execution.id';
COMMENT ON COLUMN public.auto_execution_case.plan_case_id IS '计划用例ID，对应计划与用例关系表主键';
COMMENT ON COLUMN public.auto_execution_case.case_id IS '功能用例ID，也是当前自动化与功能用例的桥梁';
COMMENT ON COLUMN public.auto_execution_case.case_key IS '用例编号快照';
COMMENT ON COLUMN public.auto_execution_case.case_title IS '用例标题快照';
COMMENT ON COLUMN public.auto_execution_case.run_order IS '执行顺序';
COMMENT ON COLUMN public.auto_execution_case.status IS '明细状态：0-待执行，1-执行中，2-通过，3-失败，4-阻塞，5-跳过，6-未找到，7-已取消';
COMMENT ON COLUMN public.auto_execution_case.pytest_nodeid IS 'pytest 节点标识，如 tests/test_xx.py::test_yy';
COMMENT ON COLUMN public.auto_execution_case.result_message IS '结果摘要';
COMMENT ON COLUMN public.auto_execution_case.error_message IS '错误信息';
COMMENT ON COLUMN public.auto_execution_case.stack_trace IS '失败堆栈';
COMMENT ON COLUMN public.auto_execution_case.report_url IS '单用例报告地址';
COMMENT ON COLUMN public.auto_execution_case.duration_seconds IS '执行耗时，单位秒';
COMMENT ON COLUMN public.auto_execution_case.started_time IS '明细开始时间';
COMMENT ON COLUMN public.auto_execution_case.finished_time IS '明细结束时间';
COMMENT ON COLUMN public.auto_execution_case.retry_count IS '重试次数';
COMMENT ON COLUMN public.auto_execution_case.ext IS '扩展字段，JSONB';
COMMENT ON COLUMN public.auto_execution_case.created_time IS '创建时间';
COMMENT ON COLUMN public.auto_execution_case.updated_time IS '更新时间';

CREATE INDEX IF NOT EXISTS idx_auto_execution_project_id ON public.auto_execution(project_id);
CREATE INDEX IF NOT EXISTS idx_auto_execution_plan_id ON public.auto_execution(plan_id);
CREATE INDEX IF NOT EXISTS idx_auto_execution_status ON public.auto_execution(status);
CREATE INDEX IF NOT EXISTS idx_auto_execution_trigger_by ON public.auto_execution(trigger_by);
CREATE INDEX IF NOT EXISTS idx_auto_execution_created_time ON public.auto_execution(created_time DESC);
CREATE INDEX IF NOT EXISTS idx_auto_execution_build_number ON public.auto_execution(jenkins_build_number);

CREATE INDEX IF NOT EXISTS idx_auto_execution_case_execution_id ON public.auto_execution_case(execution_id);
CREATE INDEX IF NOT EXISTS idx_auto_execution_case_case_id ON public.auto_execution_case(case_id);
CREATE INDEX IF NOT EXISTS idx_auto_execution_case_plan_case_id ON public.auto_execution_case(plan_case_id);
CREATE INDEX IF NOT EXISTS idx_auto_execution_case_status ON public.auto_execution_case(status);
CREATE INDEX IF NOT EXISTS idx_auto_execution_case_run_order ON public.auto_execution_case(run_order);

COMMENT ON INDEX public.idx_auto_execution_project_id IS '按项目查询执行记录索引';
COMMENT ON INDEX public.idx_auto_execution_plan_id IS '按计划查询执行记录索引';
COMMENT ON INDEX public.idx_auto_execution_status IS '按执行状态查询索引';
COMMENT ON INDEX public.idx_auto_execution_trigger_by IS '按触发人查询索引';
COMMENT ON INDEX public.idx_auto_execution_created_time IS '按创建时间倒序查询索引';
COMMENT ON INDEX public.idx_auto_execution_build_number IS '按 Jenkins 构建号查询索引';
COMMENT ON INDEX public.idx_auto_execution_case_execution_id IS '按执行主单查询明细索引';
COMMENT ON INDEX public.idx_auto_execution_case_case_id IS '按功能用例ID查询明细索引';
COMMENT ON INDEX public.idx_auto_execution_case_plan_case_id IS '按计划用例ID查询明细索引';
COMMENT ON INDEX public.idx_auto_execution_case_status IS '按明细状态查询索引';
COMMENT ON INDEX public.idx_auto_execution_case_run_order IS '按执行顺序查询索引';

CREATE OR REPLACE FUNCTION public.set_updated_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_time = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION public.set_updated_time() IS '通用更新时间触发器函数，更新 updated_time';

DROP TRIGGER IF EXISTS trg_auto_execution_updated_time ON public.auto_execution;
CREATE TRIGGER trg_auto_execution_updated_time
BEFORE UPDATE ON public.auto_execution
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_time();

DROP TRIGGER IF EXISTS trg_auto_execution_case_updated_time ON public.auto_execution_case;
CREATE TRIGGER trg_auto_execution_case_updated_time
BEFORE UPDATE ON public.auto_execution_case
FOR EACH ROW
EXECUTE FUNCTION public.set_updated_time();

COMMIT;
