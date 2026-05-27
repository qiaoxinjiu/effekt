# encoding: UTF-8
from flask import g

from .baseCrudController import BaseCrudController
from ..service.skillService import SkillService


class SkillController(BaseCrudController):
    def skill_create(self):
        return SkillService.create_skill(self.session, self.req_data, getattr(g, 'current_user_id', None))

    def skill_update(self):
        return SkillService.update_skill(self.session, self.req_data)

    def skill_delete(self):
        return SkillService.delete_skill(self.session, self.req_data)

    def skill_detail(self):
        skill_id = self._get(self.req_data, 'skillId', 'id')
        if not skill_id:
            return {}, 'skillId 为必传参数'
        return SkillService.skill_detail(self.session, skill_id)

    def skill_list(self):
        return SkillService.skill_list(self.session, self.req_data)

    def skill_rule_list(self):
        return SkillService.skill_rule_list(self.session, self.req_data)

    def business_rule_create(self):
        return SkillService.create_business_rule(self.session, self.req_data, getattr(g, 'current_user_id', None))

    def business_rule_update(self):
        return SkillService.update_business_rule(self.session, self.req_data)

    def business_rule_delete(self):
        return SkillService.delete_business_rule(self.session, self.req_data)

    def business_rule_detail(self):
        rule_id = self._get(self.req_data, 'ruleId', 'id')
        if not rule_id:
            return {}, 'ruleId 为必传参数'
        return SkillService.business_rule_detail(self.session, rule_id)

    def business_rule_list(self):
        return SkillService.business_rule_list(self.session, self.req_data)
