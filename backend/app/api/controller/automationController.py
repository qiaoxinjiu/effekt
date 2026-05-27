# encoding: UTF-8
from flask import g

from const import AUTOMATION_CALLBACK_SECRET
from .baseCrudController import BaseCrudController
from ..service.automationService import AutomationService


class AutomationController(BaseCrudController):
    def validate_callback_secret(self):
        callback_secret = self.req_data.get('_callback_secret')
        if AUTOMATION_CALLBACK_SECRET and callback_secret != AUTOMATION_CALLBACK_SECRET:
            return False, '回调鉴权失败'
        return True, ''

    def case_run(self):
        return AutomationService.create_case_execution(self.session, self.req_data, getattr(g, 'current_user_id', None))

    def plan_run(self):
        return AutomationService.create_plan_execution(self.session, self.req_data, getattr(g, 'current_user_id', None))

    def execution_list(self):
        return AutomationService.list_executions(self.session, self.req_data)

    def execution_detail(self):
        execution_id = self._get(self.req_data, 'executionId', 'id')
        if not execution_id:
            return {}, 'executionId 为必传参数'
        return AutomationService.get_execution_detail(self.session, execution_id)

    def execution_case_list(self):
        return AutomationService.list_execution_cases(self.session, self.req_data)

    def execution_case_pull(self):
        execution_id = self._get(self.req_data, 'executionId', 'execution_id')
        if not execution_id:
            return {}, 'executionId 为必传参数'
        return AutomationService.pull_execution_cases(self.session, execution_id, self.req_data.get('_callback_token'))

    def execution_queued(self):
        return AutomationService.mark_execution_queued(self.session, self.req_data)

    def execution_start(self):
        return AutomationService.mark_execution_started(self.session, self.req_data)

    def execution_case_result(self):
        return AutomationService.save_case_result(self.session, self.req_data)

    def execution_finish(self):
        return AutomationService.finish_execution(self.session, self.req_data)

    def execution_abort(self):
        return AutomationService.abort_execution(self.session, self.req_data)
