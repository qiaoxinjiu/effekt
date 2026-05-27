# encoding: UTF-8
from ..dao.planDao import PlanDao
from ..model.planModel import PlanCase, TestPlan


class PlanService(object):
    """测试计划域 Service 层，封装计划统计等业务能力。"""

    @staticmethod
    def create(session, model_cls, add_info):
        return PlanDao.create(session, model_cls, add_info)

    @staticmethod
    def batch_create(session, model_cls, batch_info_list):
        return PlanDao.batch_create(session, model_cls, batch_info_list)

    @staticmethod
    def update_by_id(session, model_cls, obj_id, update_info, soft_delete=True):
        return PlanDao.update_by_id(session, model_cls, obj_id, update_info, soft_delete)

    @staticmethod
    def get_by_id(session, model_cls, obj_id, soft_delete=True):
        return PlanDao.get_by_id(session, model_cls, obj_id, soft_delete)

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page_num=1, page_size=20, order_column=None, asc=False):
        return PlanDao.list_by_filters(session, model_cls, filter_list, int(page_num), int(page_size), order_column, asc)

    @staticmethod
    def delete_by_id(session, model_cls, obj_id):
        return PlanDao.delete_by_id(session, model_cls, obj_id)

    @staticmethod
    def plan_stats(session, plan_id):
        return PlanDao.plan_stats(session, plan_id)

    @staticmethod
    def refresh_plan_status(session, plan_id):
        total = session.query(PlanCase).filter(PlanCase.plan_id == int(plan_id)).count()
        if total == 0:
            return
        unexecuted_count = session.query(PlanCase).filter(PlanCase.plan_id == int(plan_id), PlanCase.status == 0).count()
        failed_count = session.query(PlanCase).filter(PlanCase.plan_id == int(plan_id), PlanCase.status.in_([2, 3])).count()
        plan = PlanDao.get_by_id(session, TestPlan, plan_id)
        if not plan or plan.status == 3:
            return
        if unexecuted_count == 0:
            new_status = 4 if failed_count == 0 else 2
        elif unexecuted_count < total:
            new_status = 1
        else:
            new_status = plan.status
        if new_status != plan.status:
            PlanDao.update_by_id(session, TestPlan, plan_id, {'status': new_status})
