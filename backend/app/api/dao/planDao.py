# encoding: UTF-8
from sqlalchemy import func

from ..model.planModel import PlanCase, TestPlan, TestRound
from logger import logger


class PlanDao(object):
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
    def batch_create(session, model_cls, batch_info_list):
        if not batch_info_list:
            return 0, ''
        objs = [model_cls(**info) for info in batch_info_list]
        session.add_all(objs)
        err = session.done(close=False)
        if err:
            logger.warning(f'{model_cls.__name__}批量新增失败！{err}')
            return 0, f'批量新增失败！{err}'
        return len(objs), ''

    @staticmethod
    def update_by_id(session, model_cls, obj_id, update_info, soft_delete=True):
        filters = [model_cls.id == int(obj_id)]
        if soft_delete and hasattr(model_cls, 'is_delete'):
            filters.append(model_cls.is_delete == 0)
        update_res = session.query(model_cls).filter(*filters).update(update_info)
        err = session.done(close=False)
        if err:
            logger.error(f'{model_cls.__name__}更新失败！id: {obj_id}, err: {err}')
            return 0, f'更新失败！{err}'
        if not update_res:
            return 0, '未查询到对应记录！'
        return int(obj_id), ''

    @staticmethod
    def get_by_id(session, model_cls, obj_id, soft_delete=True):
        filters = [model_cls.id == int(obj_id)]
        if soft_delete and hasattr(model_cls, 'is_delete'):
            filters.append(model_cls.is_delete == 0)
        return session.query(model_cls).filter(*filters).first()

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page=1, limit=20, order_column=None, asc=False):
        query = session.query(model_cls).filter(*filter_list)
        if hasattr(model_cls, 'is_delete'):
            query = query.filter(model_cls.is_delete == 0)
        total = query.count()
        if order_column is not None:
            query = query.order_by(order_column.asc() if asc else order_column.desc())
        rets = query.offset((int(page) - 1) * int(limit)).limit(int(limit)).all()
        return rets, total

    @staticmethod
    def delete_by_id(session, model_cls, obj_id):
        return PlanDao.update_by_id(session, model_cls, obj_id, {'is_delete': 1})

    @staticmethod
    def plan_stats(session, plan_id):
        """聚合计划执行进度，用于计划详情、进度看板和报告生成。"""
        total = session.query(func.count(PlanCase.id)).filter(PlanCase.plan_id == int(plan_id)).scalar() or 0
        passed = session.query(func.count(PlanCase.id)).filter(PlanCase.plan_id == int(plan_id), PlanCase.status == 1).scalar() or 0
        failed = session.query(func.count(PlanCase.id)).filter(PlanCase.plan_id == int(plan_id), PlanCase.status == 2).scalar() or 0
        blocked = session.query(func.count(PlanCase.id)).filter(PlanCase.plan_id == int(plan_id), PlanCase.status == 3).scalar() or 0
        completed = passed + failed + blocked
        pass_rate = round(passed / total * 100, 2) if total else 0
        return {'total_cases': total, 'completed': completed, 'passed': passed, 'failed': failed, 'blocked': blocked, 'pass_rate': pass_rate}

    @staticmethod
    def plan_model():
        return TestPlan

    @staticmethod
    def plan_case_model():
        return PlanCase

    @staticmethod
    def round_model():
        return TestRound
