from sqlalchemy import BigInteger, Column, Integer, SmallInteger, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

from common.sqlSession import to_dict

Base = declarative_base()
Base.to_dict = to_dict


class TestSkill(Base):
    __tablename__ = 'test_skill'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    project_id = Column(BigInteger, nullable=False, comment='项目id')
    module_id = Column(BigInteger, comment='模块id，空表示项目级通用')
    name = Column(String(128), nullable=False, comment='Skill名称')
    code = Column(String(64), nullable=False, comment='Skill编码，项目内唯一')
    description = Column(Text, comment='Skill描述')
    trigger_condition = Column(Text, nullable=False, comment='触发条件')
    reasoning_path = Column(Text, comment='推理路径')
    output_spec = Column(Text, comment='输出规范')
    skill_file_path = Column(String(512), comment='Skill文件路径，指向config/skills下生成的SKILL.md')
    skill_type = Column(SmallInteger, nullable=False, default=1, comment='类型：1通用测试策略 2历史缺陷模式 3边界场景 4接口测试 5UI测试 6性能测试 7安全测试 8数据一致性 9并发幂等 99其他')
    risk_level = Column(SmallInteger, nullable=False, default=2, comment='风险等级：0高 1中高 2中 3低')
    tags = Column(JSONB, nullable=False, server_default=text("'[]'::jsonb"), comment='标签数组')
    status = Column(SmallInteger, nullable=False, default=1, comment='状态：1启用 2停用 3草稿')
    owner_id = Column(BigInteger, comment='负责人用户id')
    created_by = Column(BigInteger, comment='创建人用户id')
    usage_count = Column(Integer, nullable=False, default=0, comment='使用次数')
    is_delete = Column(Integer, nullable=False, default=0, comment='0未删除 1已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), nullable=True, comment='修改时间')


class TestBusinessRule(Base):
    __tablename__ = 'test_business_rule'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    project_id = Column(BigInteger, nullable=False, comment='项目id')
    module_id = Column(BigInteger, comment='模块id，空表示项目级通用')
    name = Column(String(128), nullable=False, comment='业务规则名称')
    rule_code = Column(String(64), comment='业务规则编码，项目内唯一')
    rule_content = Column(Text, nullable=False, comment='业务规则内容')
    applicable_scene = Column(Text, comment='适用场景')
    example = Column(Text, comment='示例')
    rule_file_path = Column(String(512), comment='业务规则文件路径，指向config/rules下生成的RULE.md')
    priority = Column(SmallInteger, nullable=False, default=2, comment='优先级：0高 1中高 2中 3低')
    tags = Column(JSONB, nullable=False, server_default=text("'[]'::jsonb"), comment='标签数组')
    status = Column(SmallInteger, nullable=False, default=1, comment='状态：1启用 2停用 3草稿')
    owner_id = Column(BigInteger, comment='负责人用户id')
    created_by = Column(BigInteger, comment='创建人用户id')
    usage_count = Column(Integer, nullable=False, default=0, comment='使用次数')
    is_delete = Column(Integer, nullable=False, default=0, comment='0未删除 1已删除')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
    updated_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'), nullable=True, comment='修改时间')


class TestAiGenerationContext(Base):
    __tablename__ = 'test_ai_generation_context'
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    generation_id = Column(BigInteger, comment='AI生成任务id，兼容现有生成任务')
    project_id = Column(BigInteger, nullable=False, comment='项目id')
    module_id = Column(BigInteger, comment='模块id')
    source_type = Column(SmallInteger, nullable=False, comment='来源类型：1 Skill 2业务规则')
    source_id = Column(BigInteger, nullable=False, comment='来源id')
    source_name = Column(String(128), comment='来源名称快照')
    match_score = Column(Integer, nullable=False, default=0, comment='匹配分数')
    created_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=True, comment='创建时间')
