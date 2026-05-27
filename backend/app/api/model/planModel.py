from sqlalchemy import BigInteger, Column, Date, Integer, SmallInteger, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

from common.sqlSession import to_dict

Base = declarative_base()
Base.to_dict = to_dict


class TestPlan(Base):
    __tablename__ = 'test_plan'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    project_id = Column(BigInteger, nullable=False, comment='项目id')
    name = Column(String(128), nullable=False, comment='计划名称')
    version = Column(String(32), comment='测试版本')
    description = Column(Text, comment='描述')
    start_date = Column(Date, comment='开始日期')
    end_date = Column(Date, comment='结束日期')
    owner_id = Column(BigInteger, comment='负责人')
    status = Column(SmallInteger, default=0, comment='0:草稿 1:进行中 2:已完成 3:已归档 4：已通过')
    environment_id = Column(BigInteger, comment='环境id')
    jenkins_url = Column(String(512), comment='Jenkins构建URL')
    is_auto = Column(SmallInteger, default=0, comment='是否自动化测试计划：0-否，1-是')
    is_delete = Column(Integer, default=0, comment='0：未删除；1：已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), nullable=True, comment='修改时间')


class PlanCase(Base):
    __tablename__ = 'plan_case'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    plan_id = Column(BigInteger, nullable=False, comment='计划id')
    case_id = Column(BigInteger, nullable=False, comment='用例id')
    assignee_id = Column(BigInteger, comment='执行人')
    round_no = Column(Integer, default=1, comment='执行轮次')
    status = Column(SmallInteger, default=0, comment='0:未开始 1:通过 2:失败 3:阻塞')
    actual_result = Column(Text, comment='实际结果')
    defect_links = Column(JSONB, server_default=text("'[]'::jsonb"), comment='缺陷链接')
    attachments = Column(JSONB, server_default=text("'[]'::jsonb"), comment='附件')
    executed_time = Column(TIMESTAMP, comment='执行时间')
    execution_duration = Column(Integer, comment='执行耗时')

role_name_map = {1: '测试经理', 2: '测试工程师', 3: '开发工程师', 4: '访客'}
class TestRound(Base):
    __tablename__ = 'test_round'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    plan_id = Column(BigInteger, nullable=False, comment='计划id')
    round_no = Column(Integer, nullable=False, comment='轮次')
    name = Column(String(64), comment='轮次名称')
    start_date = Column(Date, comment='开始日期')
    end_date = Column(Date, comment='结束日期')
