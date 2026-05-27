from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String, TIMESTAMP, Text, text
from sqlalchemy.ext.declarative import declarative_base

from common.sqlSession import to_dict

Base = declarative_base()
Base.to_dict = to_dict


class Product(Base):
    __tablename__ = 'product'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    name = Column(String(128), nullable=False, comment='产品名称')
    code = Column(String(64), unique=True, nullable=False, comment='产品编码')
    description = Column(Text, comment='产品描述')
    status = Column(SmallInteger, default=1, comment='1:启用 0:禁用')
    is_delete = Column(Integer, default=0, comment='0：未删除；1：已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), nullable=True, comment='修改时间')
