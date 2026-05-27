from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

from common.sqlSession import to_dict

Base = declarative_base()
Base.to_dict = to_dict


class AutoExecution(Base):
    __tablename__ = 'auto_execution'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    execution_no = Column(String(64), nullable=False, unique=True, comment='执行编号')
    trigger_type = Column(SmallInteger, nullable=False, comment='1:单条 2:计划')
    project_id = Column(BigInteger, nullable=False, comment='项目id')
    plan_id = Column(BigInteger, comment='计划id')
    plan_round_no = Column(Integer, comment='计划轮次')
    source_case_id = Column(BigInteger, comment='单条执行来源case_id')
    env_code = Column(String(32), nullable=False, comment='环境编码')
    run_mode = Column(SmallInteger, default=1, comment='1:串行 2:并行')
    status = Column(SmallInteger, nullable=False, default=0, comment='0:待触发 1:触发中 2:排队中 3:执行中 4:成功 5:失败 6:已取消 7:触发失败 8:回调异常')
    jenkins_job_name = Column(String(128), comment='Jenkins任务名称')
    jenkins_queue_id = Column(BigInteger, comment='Jenkins队列id')
    jenkins_build_number = Column(BigInteger, comment='Jenkins构建号')
    jenkins_build_url = Column(String(512), comment='Jenkins构建地址')
    console_url = Column(String(512), comment='控制台地址')
    report_url = Column(String(512), comment='报告地址')
    total_count = Column(Integer, default=0, comment='总数')
    pending_count = Column(Integer, default=0, comment='待执行数')
    running_count = Column(Integer, default=0, comment='执行中数')
    passed_count = Column(Integer, default=0, comment='通过数')
    failed_count = Column(Integer, default=0, comment='失败数')
    blocked_count = Column(Integer, default=0, comment='阻塞数')
    skipped_count = Column(Integer, default=0, comment='跳过数')
    not_found_count = Column(Integer, default=0, comment='未找到数')
    trigger_by = Column(BigInteger, comment='触发人')
    trigger_source = Column(String(32), server_default=text("'platform'"), comment='触发来源')
    trigger_message = Column(Text, comment='触发消息/失败原因')
    start_time = Column(TIMESTAMP, comment='开始时间')
    end_time = Column(TIMESTAMP, comment='结束时间')
    duration_seconds = Column(Integer, comment='耗时秒数')
    callback_token = Column(String(128), comment='回调token')
    ext = Column(JSONB, server_default=text("'{}'::jsonb"), comment='扩展字段')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), nullable=True, comment='修改时间')


class AutoExecutionCase(Base):
    __tablename__ = 'auto_execution_case'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    execution_id = Column(BigInteger, nullable=False, comment='执行主单id')
    plan_case_id = Column(BigInteger, comment='计划用例id')
    case_id = Column(BigInteger, nullable=False, comment='用例id')
    case_key = Column(String(64), comment='用例编号快照')
    case_title = Column(String(255), comment='用例标题快照')
    run_order = Column(Integer, default=0, comment='执行顺序')
    status = Column(SmallInteger, nullable=False, default=0, comment='0:待执行 1:执行中 2:通过 3:失败 4:阻塞 5:跳过 6:未找到 7:已取消')
    pytest_nodeid = Column(String(512), comment='pytest节点标识')
    result_message = Column(Text, comment='结果摘要')
    error_message = Column(Text, comment='错误信息')
    stack_trace = Column(Text, comment='堆栈')
    report_url = Column(String(512), comment='单用例报告地址')
    duration_seconds = Column(Integer, comment='耗时秒数')
    started_time = Column(TIMESTAMP, comment='开始时间')
    finished_time = Column(TIMESTAMP, comment='结束时间')
    retry_count = Column(Integer, default=0, comment='重试次数')
    ext = Column(JSONB, server_default=text("'{}'::jsonb"), comment='扩展字段')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), nullable=True, comment='修改时间')
