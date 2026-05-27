# encoding: UTF-8
from sqlalchemy import or_

from logger import logger
from ..model.caseModel import Module
from ..model.productModel import Product
from ..model.projectModel import Project
from ..model.skillModel import TestSkill, TestBusinessRule, TestAiGenerationContext


class SkillDao(object):
    @staticmethod
    def create(session, model_cls, add_info):
        obj = model_cls(**add_info)
        session.add(obj)
        err = session.done(close=False)
        if err:
            logger.warning(f'{model_cls.__name__}新增失败！{err}')
            return 0, f'新增失败！{err}'
        return obj.id, ''

    @staticmethod
    def update_by_id(session, model_cls, obj_id, update_info):
        update_res = session.query(model_cls).filter(model_cls.id == int(obj_id), model_cls.is_delete == 0).update(update_info)
        err = session.done(close=False)
        if err:
            logger.error(f'{model_cls.__name__}更新失败！id: {obj_id}, err: {err}')
            return 0, f'更新失败！{err}'
        if not update_res:
            return 0, '未查询到对应记录！'
        return int(obj_id), ''

    @staticmethod
    def get_by_id(session, model_cls, obj_id):
        return session.query(model_cls).filter(model_cls.id == int(obj_id), model_cls.is_delete == 0).first()

    @staticmethod
    def get_skill_by_project_code(session, project_id, code):
        return session.query(TestSkill).filter(
            TestSkill.project_id == int(project_id),
            TestSkill.code == code,
            TestSkill.is_delete == 0
        ).first()

    @staticmethod
    def get_business_rule_by_project_code(session, project_id, rule_code):
        return session.query(TestBusinessRule).filter(
            TestBusinessRule.project_id == int(project_id),
            TestBusinessRule.rule_code == rule_code,
            TestBusinessRule.is_delete == 0
        ).first()

    @staticmethod
    def list_skill(session, filters, page=1, limit=20, keyword=None, tag=None):
        query = session.query(TestSkill).filter(TestSkill.is_delete == 0, *filters)
        if keyword:
            like_keyword = f'%{keyword}%'
            query = query.filter(or_(
                TestSkill.name.like(like_keyword),
                TestSkill.code.like(like_keyword),
                TestSkill.description.like(like_keyword),
                TestSkill.trigger_condition.like(like_keyword)
            ))
        if tag:
            query = query.filter(TestSkill.tags.contains([tag]))
        total = query.count()
        items = query.order_by(TestSkill.created_time.desc()).offset((int(page) - 1) * int(limit)).limit(int(limit)).all()
        return items, total

    @staticmethod
    def list_business_rule(session, filters, page=1, limit=20, keyword=None, tag=None):
        query = session.query(TestBusinessRule).filter(TestBusinessRule.is_delete == 0, *filters)
        if keyword:
            like_keyword = f'%{keyword}%'
            query = query.filter(or_(
                TestBusinessRule.name.like(like_keyword),
                TestBusinessRule.rule_code.like(like_keyword),
                TestBusinessRule.rule_content.like(like_keyword),
                TestBusinessRule.applicable_scene.like(like_keyword)
            ))
        if tag:
            query = query.filter(TestBusinessRule.tags.contains([tag]))
        total = query.count()
        items = query.order_by(TestBusinessRule.created_time.desc()).offset((int(page) - 1) * int(limit)).limit(int(limit)).all()
        return items, total

    @staticmethod
    def delete_by_id(session, model_cls, obj_id):
        return SkillDao.update_by_id(session, model_cls, obj_id, {'is_delete': 1})

    @staticmethod
    def get_project_by_product(session, product_id, project_id):
        return session.query(Project).filter(
            Project.id == int(project_id),
            Project.product_id == int(product_id),
            Project.is_delete == 0
        ).first()

    @staticmethod
    def list_skills_by_project(session, project_id, status=None):
        query = session.query(TestSkill).filter(
            TestSkill.project_id == int(project_id),
            TestSkill.is_delete == 0
        )
        if status not in (None, ''):
            query = query.filter(TestSkill.status == int(status))
        return query.order_by(TestSkill.created_time.desc()).all()

    @staticmethod
    def list_business_rules_by_project(session, project_id, status=None):
        query = session.query(TestBusinessRule).filter(
            TestBusinessRule.project_id == int(project_id),
            TestBusinessRule.is_delete == 0
        )
        if status not in (None, ''):
            query = query.filter(TestBusinessRule.status == int(status))
        return query.order_by(TestBusinessRule.created_time.desc()).all()

    @staticmethod
    def list_skills_by_ids(session, project_id, skill_ids):
        if not skill_ids:
            return []
        return session.query(TestSkill).filter(
            TestSkill.project_id == int(project_id),
            TestSkill.id.in_([int(skill_id) for skill_id in skill_ids]),
            TestSkill.is_delete == 0
        ).all()

    @staticmethod
    def list_business_rules_by_ids(session, project_id, rule_ids):
        if not rule_ids:
            return []
        return session.query(TestBusinessRule).filter(
            TestBusinessRule.project_id == int(project_id),
            TestBusinessRule.id.in_([int(rule_id) for rule_id in rule_ids]),
            TestBusinessRule.is_delete == 0
        ).all()

    @staticmethod
    def get_skill_path_context(session, project_id, module_id=None):
        project = session.query(Project).filter(Project.id == int(project_id), Project.is_delete == 0).first()
        product = None
        module = None
        if project and project.product_id:
            product = session.query(Product).filter(Product.id == int(project.product_id), Product.is_delete == 0).first()
        if module_id:
            module = session.query(Module).filter(Module.id == int(module_id), Module.is_delete == 0).first()
        return {
            'product_name': product.name if product else '未关联产品',
            'project_name': project.name if project else f'项目{project_id}',
            'module_name': module.name if module else '项目通用'
        }

    @staticmethod
    def batch_create_generation_context(session, rows):
        if not rows:
            return 0, ''
        session.add_all([TestAiGenerationContext(**row) for row in rows])
        err = session.done(close=False)
        if err:
            logger.warning(f'TestAiGenerationContext批量新增失败！{err}')
            return 0, f'批量新增失败！{err}'
        return len(rows), ''
