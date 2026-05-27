# encoding: UTF-8
from ..dao.planDao import PlanDao
from ..dao.projectDao import ProjectDao
from ..dao.reportDao import ReportDao
from ..model.planModel import TestPlan
from ..model.reportModel import Report


class ReportService(object):
    @staticmethod
    def create(session, model_cls, add_info):
        return ReportDao.create(session, model_cls, add_info)

    @staticmethod
    def get_by_id(session, model_cls, obj_id):
        return ReportDao.get_by_id(session, model_cls, obj_id)

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page_num=1, page_size=20, order_column=None, asc=False):
        return ReportDao.list_by_filters(session, model_cls, filter_list, int(page_num), int(page_size), order_column, asc)

    @staticmethod
    def generate_report(session, plan_id, generated_by=None):
        plan = PlanDao.get_by_id(session, TestPlan, plan_id)
        if not plan:
            return 0, '未查询到对应计划！'
        project = ProjectDao.get_by_id(session, ProjectDao.project_model(), plan.project_id)
        if not project:
            return 0, '未查询到对应项目！'
        # 复用计划统计，保证计划详情和报告中的指标口径一致。
        stats = PlanDao.plan_stats(session, plan_id)
        # MVP 阶段先生成简单 HTML，后续可替换为模板渲染器。
        content = '<html><body><h1>{}</h1><p>总用例：{}</p><p>通过率：{}%</p></body></html>'.format(
            plan.name, stats['total_cases'], stats['pass_rate']
        )
        add_info = {
            'plan_id': int(plan_id),
            'project_id': plan.project_id,
            'product_id': project.product_id,
            'name': '{}_报告'.format(plan.name),
            'report_type': 1,
            'summary': stats,
            'content': content,
            'generated_by': generated_by
        }
        return ReportDao.create(session, Report, add_info)
