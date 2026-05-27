from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String, Text, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

from common.sqlSession import to_dict

Base = declarative_base()
Base.to_dict = to_dict


class ProjectHook(Base):
    __tablename__ = 'project_hook'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    project_id = Column(BigInteger, nullable=False, comment='项目id')
    hook_type = Column(SmallInteger, nullable=False, comment='1:飞书 2:钉钉 3:企微')
    webhook_url = Column(String(512), nullable=False, comment='webhook地址')
    secret = Column(String(256), comment='签名密钥')
    enabled = Column(SmallInteger, default=1, comment='1:启用 0:禁用')
    description = Column(String(256), comment='描述')
    config = Column(JSONB, server_default=text("'{}'::jsonb"), comment='扩展配置')
    is_delete = Column(Integer, default=0, comment='0：未删除；1：已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), nullable=True, comment='修改时间')