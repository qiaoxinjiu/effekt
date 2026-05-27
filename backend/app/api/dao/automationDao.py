# encoding: UTF-8
from sqlalchemy import func

from logger import logger
from ..model.automationModel import AutoExecution, AutoExecutionCase
from ..model.caseModel import TestCase
from ..model.planModel import PlanCase, TestPlan


class AutomationDao(object):
    @staticmethod
    def create_execution(session, add_info):
        obj = AutoExecution(**add_info)
        session.add(obj)
        err = session.done(close=False)
        if err:
            logger.warning(f'AutoExecution新增失败！{err}')
            return 0, f'新增失败！{err}'
        return obj, ''

    @staticmethod
    def batch_create_execution_cases(session, batch_info_list):
        if not batch_info_list:
            return [], ''
        objs = [AutoExecutionCase(**info) for info in batch_info_list]
        session.add_all(objs)
        err = session.done(close=False)
        if err:
            logger.warning(f'AutoExecutionCase批量新增失败！{err}')
            return [], f'批量新增失败！{err}'
        return objs, ''

    @staticmethod
    def update_execution_by_id(session, execution_id, update_info):
        update_res = session.query(AutoExecution).filter(AutoExecution.id == int(execution_id)).update(update_info)
        err = session.done(close=False)
        if err:
            logger.error(f'AutoExecution更新失败！id: {execution_id}, err: {err}')
            return 0, f'更新失败！{err}'
        if not update_res:
            return 0, '未查询到对应执行记录！'
        return int(execution_id), ''

    @staticmethod
    def get_execution_by_id(session, execution_id):
        return session.query(AutoExecution).filter(AutoExecution.id == int(execution_id)).first()

    @staticmethod
    def list_execution_by_filters(session, filters, page=1, limit=20):
        query = session.query(AutoExecution).filter(*filters)
        total = query.count()
        items = query.order_by(AutoExecution.created_time.desc()).offset((int(page) - 1) * int(limit)).limit(int(limit)).all()
        return items, total

    @staticmethod
    def get_execution_case_by_id(session, execution_case_id):
        return session.query(AutoExecutionCase).filter(AutoExecutionCase.id == int(execution_case_id)).first()

    @staticmethod
    def get_execution_case_by_unique(session, execution_id, case_id, plan_case_id=None):
        filters = [AutoExecutionCase.execution_id == int(execution_id), AutoExecutionCase.case_id == int(case_id)]
        if plan_case_id:
            filters.append(AutoExecutionCase.plan_case_id == int(plan_case_id))
        return session.query(AutoExecutionCase).filter(*filters).order_by(AutoExecutionCase.id.asc()).first()

    @staticmethod
    def update_execution_case_by_id(session, execution_case_id, update_info):
        update_res = session.query(AutoExecutionCase).filter(AutoExecutionCase.id == int(execution_case_id)).update(update_info)
        err = session.done(close=False)
        if err:
            logger.error(f'AutoExecutionCase更新失败！id: {execution_case_id}, err: {err}')
            return 0, f'更新失败！{err}'
        if not update_res:
            return 0, '未查询到对应执行明细！'
        return int(execution_case_id), ''

    @staticmethod
    def list_execution_case_by_filters(session, filters, page=1, limit=20):
        query = session.query(AutoExecutionCase).filter(*filters)
        total = query.count()
        items = query.order_by(AutoExecutionCase.id.asc()).offset((int(page) - 1) * int(limit)).limit(int(limit)).all()
        return items, total

    @staticmethod
    def count_execution_case_summary(session, execution_id):
        rows = session.query(AutoExecutionCase.status, func.count(AutoExecutionCase.id)).filter(
            AutoExecutionCase.execution_id == int(execution_id)
        ).group_by(AutoExecutionCase.status).all()
        summary = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
        for status, count in rows:
            summary[int(status)] = int(count)
        summary['total'] = sum(summary.values())
        return summary

    @staticmethod
    def query_case_auto_item(session, case_id):
        return session.query(TestCase).filter(
            TestCase.id == int(case_id), TestCase.is_delete == 0, TestCase.is_auto == 1
        ).first()

    @staticmethod
    def query_plan_auto_cases(session, plan_id, round_no=None, case_ids=None):
        query = session.query(PlanCase, TestCase).join(
            TestCase, PlanCase.case_id == TestCase.id
        ).filter(
            PlanCase.plan_id == int(plan_id),
            TestCase.is_delete == 0,
            TestCase.is_auto == 1
        )
        if round_no not in (None, ''):
            query = query.filter(PlanCase.round_no == int(round_no))
        if case_ids:
            query = query.filter(PlanCase.case_id.in_([int(case_id) for case_id in case_ids]))
        return query.order_by(PlanCase.id.asc()).all()

    @staticmethod
    def update_plan_case_result(session, plan_case_id, update_info):
        update_res = session.query(PlanCase).filter(PlanCase.id == int(plan_case_id)).update(update_info)
        err = session.done(close=False)
        if err:
            logger.error(f'PlanCase更新失败！id: {plan_case_id}, err: {err}')
            return 0, f'更新失败！{err}'
        if not update_res:
            return 0, '未查询到对应计划用例！'
        return int(plan_case_id), ''

    @staticmethod
    def get_plan_by_id(session, plan_id):
        return session.query(TestPlan).filter(TestPlan.id == int(plan_id), TestPlan.is_delete == 0).first()
