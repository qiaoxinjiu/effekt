from sqlalchemy import BigInteger, Boolean, Column, Integer, SmallInteger, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

from common.sqlSession import to_dict

Base = declarative_base()
Base.to_dict = to_dict


class Project(Base):
    __tablename__ = 'project'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    key = Column(String(32), unique=True, nullable=False, comment='项目唯一标识')
    name = Column(String(128), nullable=False, comment='项目名称')
    product_id = Column(Integer, comment='产品id')
    description = Column(Text, comment='项目描述')
    department = Column(String(64), comment='部门')
    status = Column(SmallInteger, default=1, comment='1:启用 0:禁用')
    config = Column(JSONB, server_default=text("'{}'::jsonb"), comment='扩展配置')
    created_by = Column(BigInteger, comment='创建人')
    is_delete = Column(Integer, default=0, comment='0：未删除；1：已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), nullable=True, comment='修改时间')


class ProjectMember(Base):
    __tablename__ = 'project_member'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    project_id = Column(BigInteger, nullable=False, comment='项目id')
    user_id = Column(BigInteger, nullable=False, comment='用户id')
    role = Column(SmallInteger, nullable=False, comment='1:测试经理 2:测试工程师 3:开发工程师 4:访客')
    joined_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='加入时间')


class Environment(Base):
    __tablename__ = 'environment'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    project_id = Column(BigInteger, nullable=False, comment='项目id')
    name = Column(String(64), nullable=False, comment='环境名称，如 dev/st/pre/prod')
    variables = Column(JSONB, nullable=False, comment='环境变量')
    is_encrypted = Column(Boolean, default=False, comment='是否加密')
    is_delete = Column(Integer, default=0, comment='0：未删除；1：已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
