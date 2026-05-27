from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String, Text, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

from common.sqlSession import to_dict

Base = declarative_base()
Base.to_dict = to_dict


class Bug(Base):
    __tablename__ = 'bug'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    bug_key = Column(String(64), nullable=False, unique=True)
    title = Column(String(256), nullable=False)
    description = Column(Text)
    bug_type = Column(SmallInteger, nullable=False, default=1)
    severity = Column(SmallInteger, nullable=False, default=2)
    priority = Column(SmallInteger, nullable=False, default=2)
    status = Column(SmallInteger, nullable=False, default=0)
    assignee_id = Column(BigInteger)
    reporter_id = Column(BigInteger, nullable=False)
    product_id = Column(BigInteger, nullable=False)
    project_id = Column(BigInteger, nullable=False)
    module_id = Column(BigInteger)
    case_id = Column(BigInteger)
    plan_id = Column(BigInteger)
    environment = Column(String(64))
    steps = Column(Text)
    solution = Column(Text)
    resolve_version = Column(String(64))
    resolved_by = Column(BigInteger)
    reproduce_rate = Column(SmallInteger)
    attachments = Column(JSONB, server_default=text("'[]'::jsonb"))
    is_delete = Column(Integer, default=0)
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True)
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), nullable=True)


class BugComment(Base):
    __tablename__ = 'bug_comment'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    bug_id = Column(BigInteger, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    is_delete = Column(Integer, default=0)
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True)


class BugHistory(Base):
    __tablename__ = 'bug_history'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    bug_id = Column(BigInteger, nullable=False)
    field_name = Column(String(64), nullable=False)
    old_value = Column(String(512))
    new_value = Column(String(512))
    operator_id = Column(BigInteger, nullable=False)
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True)