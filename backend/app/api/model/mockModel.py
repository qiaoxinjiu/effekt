# encoding: UTF-8
from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String, TIMESTAMP, Text, text
from sqlalchemy.ext.declarative import declarative_base

from common.sqlSession import to_dict

Base = declarative_base()
Base.to_dict = to_dict


class MockDocument(Base):
    __tablename__ = 'mock_document'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    product_id = Column(BigInteger, nullable=False, comment='产品ID')
    project_id = Column(BigInteger, nullable=False, comment='项目ID')
    name = Column(String(255), nullable=False, comment='文档名称')
    source_type = Column(String(32), nullable=False, comment='来源类型：openapi/apifox/yapi/markdown/text/pdf/word/manual')
    source = Column(String(512), comment='文件路径、URL或来源说明')
    content = Column(Text, comment='文档文本内容或原始JSON')
    parse_status = Column(SmallInteger, default=0, comment='解析状态：0-待解析，1-解析成功，2-解析失败，3-部分成功')
    parse_error = Column(Text, comment='整体解析错误')
    interface_count = Column(Integer, default=0, comment='成功解析接口数量')
    created_by = Column(BigInteger, comment='创建人ID')
    is_delete = Column(Integer, default=0, comment='0：未删除；1：已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), comment='更新时间')


class MockInterface(Base):
    __tablename__ = 'mock_interface'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    document_id = Column(BigInteger, comment='来源文档ID')
    product_id = Column(BigInteger, nullable=False, comment='产品ID')
    project_id = Column(BigInteger, nullable=False, comment='项目ID')
    name = Column(String(255), nullable=False, comment='接口名称')
    path = Column(String(512), nullable=False, comment='接口路径')
    method = Column(String(16), nullable=False, comment='请求方法')
    description = Column(Text, comment='接口描述')
    headers_schema = Column(Text, comment='请求头Schema JSON')
    query_schema = Column(Text, comment='Query Schema JSON')
    body_schema = Column(Text, comment='Body Schema JSON')
    response_schema = Column(Text, comment='Response Schema JSON')
    raw_schema = Column(Text, comment='统一Schema JSON')
    path_regex = Column(String(1024), comment='动态路径匹配正则')
    path_params = Column(Text, comment='动态路径参数JSON')
    path_score = Column(Integer, default=0, comment='路径匹配优先级')
    status = Column(SmallInteger, default=0, comment='状态：0-草稿，1-已启用，2-已停用')
    created_by = Column(BigInteger, comment='创建人ID')
    is_delete = Column(Integer, default=0, comment='0：未删除；1：已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), comment='更新时间')


class MockScene(Base):
    __tablename__ = 'mock_scene'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    interface_id = Column(BigInteger, nullable=False, comment='接口ID')
    scene_name = Column(String(128), nullable=False, comment='场景名称')
    scene_code = Column(String(64), nullable=False, comment='场景编码')
    http_status = Column(Integer, default=200, comment='HTTP状态码')
    delay_ms = Column(Integer, default=0, comment='响应延迟毫秒')
    request_example = Column(Text, comment='请求示例JSON')
    response_template = Column(Text, comment='响应模板JSON')
    response_headers = Column(Text, comment='响应Header JSON')
    response_rule = Column(Text, comment='响应规则JSON')
    match_rule = Column(Text, comment='匹配规则JSON')
    priority = Column(Integer, default=0, comment='场景优先级，越大越优先')
    status = Column(SmallInteger, default=0, comment='状态：0-草稿，1-已启用，2-已停用')
    is_delete = Column(Integer, default=0, comment='0：未删除；1：已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), comment='更新时间')


class MockCallLog(Base):
    __tablename__ = 'mock_call_log'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    project_id = Column(BigInteger, nullable=False, comment='项目ID')
    interface_id = Column(BigInteger, comment='接口ID')
    scene_id = Column(BigInteger, comment='场景ID')
    method = Column(String(16), nullable=False, comment='请求方法')
    path = Column(String(512), nullable=False, comment='请求路径')
    request_query = Column(Text, comment='Query参数JSON')
    request_body = Column(Text, comment='Body参数JSON')
    response_body = Column(Text, comment='响应内容JSON')
    http_status = Column(Integer, default=200, comment='HTTP状态码')
    duration_ms = Column(Integer, default=0, comment='请求耗时毫秒')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')


class MockParseIssue(Base):
    __tablename__ = 'mock_parse_issue'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    document_id = Column(BigInteger, nullable=False, comment='文档ID')
    issue_type = Column(String(64), nullable=False, comment='问题类型')
    source_fragment = Column(Text, comment='失败片段')
    error_message = Column(Text, comment='错误信息')
    suggestion = Column(Text, comment='修复建议')
    status = Column(SmallInteger, default=0, comment='状态：0-未处理，1-已处理，2-已忽略')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), comment='更新时间')
