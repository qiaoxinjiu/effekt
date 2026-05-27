from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

from common.sqlSession import to_dict

Base = declarative_base()
Base.to_dict = to_dict


class UpdateSqlProject(Base):
    __tablename__ = 'update_sql_project'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    sql = Column(String(500), comment='sql语句')
    run_env = Column(String(120), comment='运行环境')
    project = Column(String(120), comment='项目')
    run_group = Column(String(120), comment='对sql进行分组')
    remark = Column(String(300), comment='备注')
    creator = Column(String(300), comment='创建人')
    is_delete = Column(Integer, default=0, comment='0：未删除；1：已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
    modified_time = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP'),
        server_onupdate=text('CURRENT_TIMESTAMP'),
        nullable=True,
        comment='修改时间'
    )
