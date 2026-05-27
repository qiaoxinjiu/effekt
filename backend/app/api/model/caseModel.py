from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.ext.declarative import declarative_base

from common.sqlSession import to_dict

Base = declarative_base()
Base.to_dict = to_dict


class Module(Base):
    __tablename__ = 'module'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    project_id = Column(BigInteger, nullable=False, comment='项目id')
    parent_id = Column(BigInteger, default=0, comment='父模块id')
    name = Column(String(128), nullable=False, comment='模块名称')
    sort_order = Column(Integer, default=0, comment='排序')
    path = Column(String(512), comment='模块路径')
    is_delete = Column(Integer, default=0, comment='0：未删除；1：已删除')
    status = Column(Integer, default=0, comment='0：待确认；1：正常；2：弃用')


class TestCase(Base):
    __tablename__ = 'test_case'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    project_id = Column(BigInteger, nullable=False, comment='项目id')
    module_id = Column(BigInteger, comment='模块id')
    case_key = Column(String(64), nullable=False, comment='项目内唯一编号')
    title = Column(String(255), nullable=False, comment='标题')
    preconditions = Column(Text, comment='前置条件')
    steps = Column(Text, comment='步骤')
    expected_results = Column(Text, comment='预期结果')
    priority = Column(SmallInteger, default=2, comment='0:P0 1:P1 2:P2 3:P3')
    case_type = Column(SmallInteger, default=1, comment='1:功能 2:性能 3:安全 4:接口')
    tags = Column(ARRAY(String(64)), server_default=text("'{}'::varchar[]"), comment='标签')
    status = Column(SmallInteger, default=1, comment='1:正常 2:已废弃 3:评审中 4：评审通过')
    is_auto = Column(Integer, default=0, comment='0：未实现自动化；1：已实现自动化')
    is_ai_generated = Column(Integer, default=0, comment='0：非AI生成；1：AI生成')
    created_by = Column(BigInteger, comment='创建人')
    is_delete = Column(Integer, default=0, comment='0：未删除；1：已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), nullable=True, comment='修改时间')


class CaseSnapshot(Base):
    __tablename__ = 'case_snapshot'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    case_id = Column(BigInteger, nullable=False, comment='用例id')
    version = Column(Integer, nullable=False, comment='版本')
    snapshot = Column(JSONB, nullable=False, comment='快照')
    created_by = Column(BigInteger, comment='创建人')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')


class CaseReview(Base):
    __tablename__ = 'case_review'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    case_id = Column(BigInteger, nullable=False, comment='用例id')
    reviewer_id = Column(BigInteger, nullable=False, comment='评审人')
    status = Column(SmallInteger, default=0, comment='0:待评审 1:通过 2:驳回 3:建议修改')
    comments = Column(Text, comment='评论')
    diff_content = Column(Text, comment='JSON diff')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
    reviewed_time = Column(TIMESTAMP, nullable=True, comment='评审时间')
