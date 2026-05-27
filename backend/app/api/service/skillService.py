# encoding: UTF-8
import re
import shutil
from datetime import datetime
from pathlib import Path

from ..dao.skillDao import SkillDao
from ..model.skillModel import TestSkill, TestBusinessRule
from .aiService import AIService


class SkillService(object):
    VALID_SKILL_TYPES = {1, 2, 3, 4, 5, 6, 7, 8, 9, 99}
    VALID_STATUS = {1, 2, 3}
    VALID_LEVELS = {0, 1, 2, 3}

    @staticmethod
    def _get(req_data, *keys, default=None):
        for key in keys:
            value = req_data.get(key)
            if value not in (None, ''):
                return value
        return default

    @staticmethod
    def _ensure_list(value, field_name):
        if value in (None, ''):
            return [], ''
        if not isinstance(value, list):
            return [], f'{field_name} 必须是数组'
        return value, ''

    @staticmethod
    def _normalize_generated_tags(value, fallback):
        if isinstance(value, list):
            tags = [str(item).strip() for item in value if str(item).strip()]
        elif isinstance(value, str):
            tags = [item.strip() for item in re.split(r'[,，、\s]+', value) if item.strip()]
        else:
            tags = []
        return tags[:8] or fallback

    @staticmethod
    def _generate_unique_code(session, project_id, name, prefix, exists_checker):
        name_text = str(name or '').strip().upper()
        letters = re.sub(r'[^A-Z0-9]+', '_', name_text).strip('_')
        code_prefix = (letters[:24] if letters else prefix) or prefix
        time_part = datetime.now().strftime('%Y%m%d%H%M%S%f')[:20]
        code = f'{code_prefix}_{time_part}'[:64]
        if not exists_checker(session, project_id, code):
            return code
        for index in range(1, 100):
            candidate = f'{code_prefix}_{time_part}_{index}'[:64]
            if not exists_checker(session, project_id, candidate):
                return candidate
        return f'{prefix}_{time_part}'[:64]

    @staticmethod
    def _generate_skill_code(session, project_id, name):
        return SkillService._generate_unique_code(session, project_id, name, 'SKILL', SkillDao.get_skill_by_project_code)

    @staticmethod
    def _generate_rule_code(session, project_id, name):
        return SkillService._generate_unique_code(session, project_id, name, 'RULE', SkillDao.get_business_rule_by_project_code)

    @staticmethod
    def _safe_path_name(value, fallback):
        value = str(value or '').strip() or fallback
        value = re.sub(r'[\\/:*?"<>|\r\n\t]+', '_', value)
        value = re.sub(r'\s+', ' ', value).strip(' .')
        return (value or fallback)[:80]

    @staticmethod
    def _build_rule_file_content(rule_info):
        tags = rule_info.get('tags') or []
        tags_text = ', '.join([str(tag) for tag in tags])
        frontmatter_name = re.sub(r'[^a-zA-Z0-9_-]+', '-', str(rule_info.get('name') or 'generated-rule').lower()).strip('-') or 'generated-rule'
        description = rule_info.get('rule_content') or rule_info.get('description') or rule_info.get('name') or ''
        return f'''---
name: {frontmatter_name}
description: {description}
---

# {rule_info.get('name')}

## Rule
{rule_info.get('rule_content') or ''}

## Applicable scene
{rule_info.get('applicable_scene') or ''}

## Example
{rule_info.get('example') or ''}

## Test design constraints
- Generate cases that verify this rule is satisfied in normal flows.
- Generate negative and boundary cases when the rule describes validation, limits, state changes, permissions, or data constraints.
- Mark missing prerequisites as “待确认” instead of inventing behavior.

## Metadata
- Code: {rule_info.get('rule_code') or ''}
- Product: {rule_info.get('product_name') or ''}
- Project: {rule_info.get('project_name') or ''}
- Module: {rule_info.get('module_name') or ''}
- Priority: {rule_info.get('priority')}
- Tags: {tags_text}
'''

    @staticmethod
    def _build_skill_file_content(skill_info):
        skill_md = skill_info.get('skill_md') or skill_info.get('skillMd')
        if isinstance(skill_md, str) and skill_md.strip():
            return skill_md.strip() + '\n'
        tags = skill_info.get('tags') or []
        tags_text = ', '.join([str(tag) for tag in tags])
        frontmatter_name = re.sub(r'[^a-zA-Z0-9_-]+', '-', str(skill_info.get('name') or 'generated-skill').lower()).strip('-') or 'generated-skill'
        description = skill_info.get('description') or skill_info.get('name') or ''
        return f'''---
name: {frontmatter_name}
description: {description}
---

# {skill_info.get('name')}

Use this skill when PRD, requirement, user story, interface specification, UI interaction, or business rule content needs to be transformed into high-quality test cases. This skill helps the model apply project-specific testing experience when designing functional, interface, boundary, exception, and regression cases.

## When to use this skill
{skill_info.get('trigger_condition') or ''}

## Analysis workflow
{skill_info.get('reasoning_path') or ''}

## Test design guidance
- Identify the core business flow, state changes, inputs, outputs, permissions, and data dependencies.
- Cover normal paths, boundary values, invalid inputs, exception handling, idempotency, concurrency, and regression risks when applicable.
- Mark missing or ambiguous requirements as “待确认” rather than inventing behavior.

## Output format
{skill_info.get('output_spec') or ''}

## Metadata
- Code: {skill_info.get('code') or ''}
- Product: {skill_info.get('product_name') or ''}
- Project: {skill_info.get('project_name') or ''}
- Module: {skill_info.get('module_name') or ''}
- Skill Type: {skill_info.get('skill_type')}
- Risk Level: {skill_info.get('risk_level')}
- Tags: {tags_text}
'''


    @staticmethod
    def _create_asset_file(session, project_id, module_id, asset_info, root_folder, folder_name, file_name, content_builder):
        context = SkillDao.get_skill_path_context(session, project_id, module_id)
        product_name = SkillService._safe_path_name(context.get('product_name'), '未关联产品')
        project_name = SkillService._safe_path_name(context.get('project_name'), f'项目{project_id}')
        module_name = SkillService._safe_path_name(context.get('module_name'), '项目通用')
        asset_name = SkillService._safe_path_name(folder_name, '未命名')
        base_dir = Path(__file__).resolve().parents[3] / 'config' / root_folder
        asset_dir = base_dir / product_name / project_name / module_name / asset_name
        if asset_dir.exists():
            suffix = datetime.now().strftime('%Y%m%d%H%M%S%f')[:20]
            asset_dir = asset_dir.with_name(f'{asset_dir.name}_{suffix}')
        asset_dir.mkdir(parents=True, exist_ok=False)
        asset_path = asset_dir / file_name
        file_info = dict(asset_info)
        file_info.update({
            'product_name': context.get('product_name'),
            'project_name': context.get('project_name'),
            'module_name': context.get('module_name')
        })
        asset_path.write_text(content_builder(file_info), encoding='utf-8')
        return str(asset_path), str(asset_dir)

    @staticmethod
    def _create_skill_file(session, project_id, module_id, skill_info):
        return SkillService._create_asset_file(
            session, project_id, module_id, skill_info, 'skills', skill_info.get('name'), 'SKILL.md', SkillService._build_skill_file_content
        )

    @staticmethod
    def _create_rule_file(session, project_id, module_id, rule_info):
        return SkillService._create_asset_file(
            session, project_id, module_id, rule_info, 'rules', rule_info.get('name'), 'RULE.md', SkillService._build_rule_file_content
        )

    @staticmethod
    def _remove_asset_file_path(asset_file_path, root_folder):
        if not asset_file_path:
            return
        asset_path = Path(asset_file_path)
        base_dir = Path(__file__).resolve().parents[3] / 'config' / root_folder
        try:
            resolved_asset_path = asset_path.resolve()
            resolved_base_dir = base_dir.resolve()
            if resolved_base_dir not in resolved_asset_path.parents:
                return
            asset_dir = resolved_asset_path.parent
            if asset_dir.exists() and asset_dir.name not in {root_folder, 'config'}:
                shutil.rmtree(asset_dir)
        except FileNotFoundError:
            return

    @staticmethod
    def _remove_skill_file_path(skill_file_path):
        SkillService._remove_asset_file_path(skill_file_path, 'skills')

    @staticmethod
    def _remove_rule_file_path(rule_file_path):
        SkillService._remove_asset_file_path(rule_file_path, 'rules')

    @staticmethod
    def create_skill(session, req_data, user_id=None):
        project_id = SkillService._get(req_data, 'projectId', 'project_id')
        name = SkillService._get(req_data, 'name')
        if not project_id or not name:
            return 0, 'projectId、name 为必传参数'
        input_tags, err_msg = SkillService._ensure_list(SkillService._get(req_data, 'tags', default=[]), 'tags')
        if err_msg:
            return 0, err_msg

        generated_info, err_msg = AIService.generate_skill_content(req_data)
        if err_msg:
            return 0, err_msg

        generated_skill_type = generated_info.get('skill_type') or generated_info.get('skillType')
        generated_risk_level = generated_info.get('risk_level') or generated_info.get('riskLevel')
        skill_type = int(generated_skill_type if generated_skill_type is not None else SkillService._get(req_data, 'skillType', 'skill_type', default=1))
        risk_level = int(generated_risk_level if generated_risk_level is not None else SkillService._get(req_data, 'riskLevel', 'risk_level', default=2))
        status = int(SkillService._get(req_data, 'status', default=1))
        if skill_type not in SkillService.VALID_SKILL_TYPES:
            skill_type = 1
        if risk_level not in SkillService.VALID_LEVELS:
            risk_level = 2
        if status not in SkillService.VALID_STATUS:
            return 0, 'status 不合法'

        generated_tags = SkillService._normalize_generated_tags(generated_info.get('tags'), input_tags)
        module_id_value = SkillService._get(req_data, 'moduleId', 'module_id')
        module_id = int(module_id_value) if module_id_value else None
        add_info = {
            'project_id': int(project_id),
            'module_id': module_id,
            'name': name,
            'code': SkillService._generate_skill_code(session, project_id, name),
            'description': generated_info.get('description') or SkillService._get(req_data, 'description') or name,
            'trigger_condition': AIService.get_default_case_generation_trigger_condition(),
            'reasoning_path': generated_info.get('reasoning_path') or generated_info.get('reasoningPath'),
            'output_spec': AIService.get_default_case_generation_output_spec(),
            'skill_type': skill_type,
            'risk_level': risk_level,
            'tags': generated_tags,
            'status': status,
            'owner_id': int(user_id) if user_id else None,
            'created_by': user_id,
            'usage_count': 0,
            'is_delete': 0
        }
        skill_file_info = dict(add_info)
        skill_file_info['skill_md'] = generated_info.get('skill_md')
        skill_file_path, skill_dir = SkillService._create_skill_file(session, int(project_id), module_id, skill_file_info)
        add_info['skill_file_path'] = skill_file_path
        obj_id, create_err = SkillDao.create(session, TestSkill, add_info)
        if create_err:
            shutil.rmtree(skill_dir, ignore_errors=True)
            return 0, create_err
        return obj_id, ''

    @staticmethod
    def update_skill(session, req_data):
        skill_id = SkillService._get(req_data, 'skillId', 'id')
        if not skill_id:
            return 0, 'skillId 为必传参数'
        item = SkillDao.get_by_id(session, TestSkill, skill_id)
        if not item:
            return 0, '未查询到对应 Skill'
        update_info = {}
        mapping = [
            ('name', 'name'), ('description', 'description'),
            ('triggerCondition', 'trigger_condition'), ('trigger_condition', 'trigger_condition'),
            ('reasoningPath', 'reasoning_path'), ('reasoning_path', 'reasoning_path'),
            ('outputSpec', 'output_spec'), ('output_spec', 'output_spec')
        ]
        for req_key, column_key in mapping:
            value = SkillService._get(req_data, req_key)
            if value is not None:
                update_info[column_key] = value
        module_id = SkillService._get(req_data, 'moduleId', 'module_id')
        if module_id is not None:
            update_info['module_id'] = int(module_id) if module_id != '' else None
        owner_id = SkillService._get(req_data, 'ownerId', 'owner_id')
        if owner_id is not None:
            update_info['owner_id'] = int(owner_id) if owner_id != '' else None
        tags = SkillService._get(req_data, 'tags')
        if tags is not None:
            tags, err_msg = SkillService._ensure_list(tags, 'tags')
            if err_msg:
                return 0, err_msg
            update_info['tags'] = tags
        for req_key, column_key, valid_set in [
            ('skillType', 'skill_type', SkillService.VALID_SKILL_TYPES),
            ('skill_type', 'skill_type', SkillService.VALID_SKILL_TYPES),
            ('riskLevel', 'risk_level', SkillService.VALID_LEVELS),
            ('risk_level', 'risk_level', SkillService.VALID_LEVELS),
            ('status', 'status', SkillService.VALID_STATUS)
        ]:
            value = SkillService._get(req_data, req_key)
            if value is not None:
                value = int(value)
                if value not in valid_set:
                    return 0, f'{req_key} 不合法'
                update_info[column_key] = value
        if not update_info:
            return int(skill_id), ''

        merged_info = item.to_dict()
        merged_info.update(update_info)
        new_skill_file_path = None
        new_skill_dir = None
        try:
            new_skill_file_path, new_skill_dir = SkillService._create_skill_file(
                session,
                int(merged_info.get('project_id')),
                merged_info.get('module_id'),
                merged_info
            )
            update_info['skill_file_path'] = new_skill_file_path
        except Exception as e:
            return 0, f'Skill 文件创建失败：{str(e)}'

        obj_id, err_msg = SkillDao.update_by_id(session, TestSkill, skill_id, update_info)
        if err_msg:
            if new_skill_dir:
                shutil.rmtree(new_skill_dir, ignore_errors=True)
            return obj_id, err_msg
        SkillService._remove_skill_file_path(item.skill_file_path)
        return obj_id, ''

    @staticmethod
    def delete_skill(session, req_data):
        skill_id = SkillService._get(req_data, 'skillId', 'id')
        if not skill_id:
            return 0, 'skillId 为必传参数'
        item = SkillDao.get_by_id(session, TestSkill, skill_id)
        if not item:
            return 0, '未查询到对应 Skill'
        obj_id, err_msg = SkillDao.delete_by_id(session, TestSkill, skill_id)
        if err_msg:
            return obj_id, err_msg
        SkillService._remove_skill_file_path(item.skill_file_path)
        return obj_id, ''

    @staticmethod
    def skill_detail(session, skill_id):
        item = SkillDao.get_by_id(session, TestSkill, skill_id)
        if not item:
            return {}, '未查询到对应 Skill'
        return item.to_dict(), ''

    @staticmethod
    def skill_list(session, req_data):
        filters = []
        project_id = SkillService._get(req_data, 'projectId', 'project_id')
        module_id = SkillService._get(req_data, 'moduleId', 'module_id')
        status = SkillService._get(req_data, 'status')
        skill_type = SkillService._get(req_data, 'skillType', 'skill_type')
        risk_level = SkillService._get(req_data, 'riskLevel', 'risk_level')
        if project_id:
            filters.append(TestSkill.project_id == int(project_id))
        if module_id not in (None, ''):
            filters.append(TestSkill.module_id == int(module_id))
        if status not in (None, ''):
            filters.append(TestSkill.status == int(status))
        if skill_type not in (None, ''):
            filters.append(TestSkill.skill_type == int(skill_type))
        if risk_level not in (None, ''):
            filters.append(TestSkill.risk_level == int(risk_level))
        items, total = SkillDao.list_skill(
            session, filters,
            SkillService._get(req_data, 'pageNo', 'page', default=1),
            SkillService._get(req_data, 'pageSize', 'size', default=20),
            SkillService._get(req_data, 'keyword'),
            SkillService._get(req_data, 'tag')
        )
        return {'list': [item.to_dict() for item in items], 'total': total}

    @staticmethod
    def create_business_rule(session, req_data, user_id=None):
        project_id = SkillService._get(req_data, 'projectId', 'project_id')
        name = SkillService._get(req_data, 'name')
        if not project_id or not name:
            return 0, 'projectId、name 为必传参数'
        input_tags, err_msg = SkillService._ensure_list(SkillService._get(req_data, 'tags', default=[]), 'tags')
        if err_msg:
            return 0, err_msg

        generated_info, err_msg = AIService.generate_business_rule_content(req_data)
        if err_msg:
            return 0, err_msg

        input_priority = SkillService._get(req_data, 'priority')
        priority_value = input_priority if input_priority is not None else generated_info.get('priority')
        priority = int(priority_value if priority_value is not None else 2)
        status = int(SkillService._get(req_data, 'status', default=1))
        if priority not in SkillService.VALID_LEVELS:
            priority = 2
        if status not in SkillService.VALID_STATUS:
            return 0, 'status 不合法'

        generated_tags = SkillService._normalize_generated_tags(generated_info.get('tags'), input_tags)
        module_id_value = SkillService._get(req_data, 'moduleId', 'module_id')
        module_id = int(module_id_value) if module_id_value else None
        input_rule_content = SkillService._get(req_data, 'ruleContent', 'rule_content') or SkillService._get(req_data, 'description') or name
        add_info = {
            'project_id': int(project_id),
            'module_id': module_id,
            'name': name,
            'rule_code': SkillService._generate_rule_code(session, project_id, name),
            'rule_content': input_rule_content,
            'applicable_scene': SkillService._get(req_data, 'applicableScene', 'applicable_scene') or generated_info.get('applicable_scene') or generated_info.get('applicableScene'),
            'example': SkillService._get(req_data, 'example') or generated_info.get('example'),
            'priority': priority,
            'tags': input_tags or generated_tags,
            'status': status,
            'owner_id': int(user_id) if user_id else None,
            'created_by': user_id,
            'usage_count': 0,
            'is_delete': 0
        }
        rule_file_info = dict(add_info)
        rule_file_path, rule_dir = SkillService._create_rule_file(session, int(project_id), module_id, rule_file_info)
        add_info['rule_file_path'] = rule_file_path
        obj_id, create_err = SkillDao.create(session, TestBusinessRule, add_info)
        if create_err:
            shutil.rmtree(rule_dir, ignore_errors=True)
            return 0, create_err
        return obj_id, ''

    @staticmethod
    def update_business_rule(session, req_data):
        rule_id = SkillService._get(req_data, 'ruleId', 'id')
        if not rule_id:
            return 0, 'ruleId 为必传参数'
        item = SkillDao.get_by_id(session, TestBusinessRule, rule_id)
        if not item:
            return 0, '未查询到对应业务规则'
        update_info = {}
        mapping = [
            ('name', 'name'), ('ruleContent', 'rule_content'), ('rule_content', 'rule_content'),
            ('applicableScene', 'applicable_scene'), ('applicable_scene', 'applicable_scene'),
            ('example', 'example')
        ]
        for req_key, column_key in mapping:
            value = SkillService._get(req_data, req_key)
            if value is not None:
                update_info[column_key] = value
        module_id = SkillService._get(req_data, 'moduleId', 'module_id')
        if module_id is not None:
            update_info['module_id'] = int(module_id) if module_id != '' else None
        owner_id = SkillService._get(req_data, 'ownerId', 'owner_id')
        if owner_id is not None:
            update_info['owner_id'] = int(owner_id) if owner_id != '' else None
        tags = SkillService._get(req_data, 'tags')
        if tags is not None:
            tags, err_msg = SkillService._ensure_list(tags, 'tags')
            if err_msg:
                return 0, err_msg
            update_info['tags'] = tags
        priority = SkillService._get(req_data, 'priority')
        if priority is not None:
            priority = int(priority)
            if priority not in SkillService.VALID_LEVELS:
                return 0, 'priority 不合法'
            update_info['priority'] = priority
        status = SkillService._get(req_data, 'status')
        if status is not None:
            status = int(status)
            if status not in SkillService.VALID_STATUS:
                return 0, 'status 不合法'
            update_info['status'] = status
        if not update_info:
            return int(rule_id), ''

        merged_info = item.to_dict()
        merged_info.update(update_info)
        new_rule_file_path = None
        new_rule_dir = None
        try:
            new_rule_file_path, new_rule_dir = SkillService._create_rule_file(
                session,
                int(merged_info.get('project_id')),
                merged_info.get('module_id'),
                merged_info
            )
            update_info['rule_file_path'] = new_rule_file_path
        except Exception as e:
            return 0, f'业务规则文件创建失败：{str(e)}'

        obj_id, err_msg = SkillDao.update_by_id(session, TestBusinessRule, rule_id, update_info)
        if err_msg:
            if new_rule_dir:
                shutil.rmtree(new_rule_dir, ignore_errors=True)
            return obj_id, err_msg
        SkillService._remove_rule_file_path(item.rule_file_path)
        return obj_id, ''

    @staticmethod
    def delete_business_rule(session, req_data):
        rule_id = SkillService._get(req_data, 'ruleId', 'id')
        if not rule_id:
            return 0, 'ruleId 为必传参数'
        item = SkillDao.get_by_id(session, TestBusinessRule, rule_id)
        if not item:
            return 0, '未查询到对应业务规则'
        obj_id, err_msg = SkillDao.delete_by_id(session, TestBusinessRule, rule_id)
        if err_msg:
            return obj_id, err_msg
        SkillService._remove_rule_file_path(item.rule_file_path)
        return obj_id, ''

    @staticmethod
    def business_rule_detail(session, rule_id):
        item = SkillDao.get_by_id(session, TestBusinessRule, rule_id)
        if not item:
            return {}, '未查询到对应业务规则'
        return item.to_dict(), ''

    @staticmethod
    def skill_rule_list(session, req_data):
        product_id = SkillService._get(req_data, 'productId', 'product_id')
        project_id = SkillService._get(req_data, 'projectId', 'project_id')
        status = SkillService._get(req_data, 'status')
        if not product_id or not project_id:
            return {}, 'productId、projectId 为必传参数'
        project = SkillDao.get_project_by_product(session, product_id, project_id)
        if not project:
            return {}, '未查询到对应产品下的项目'
        skills = SkillDao.list_skills_by_project(session, project_id, status)
        rules = SkillDao.list_business_rules_by_project(session, project_id, status)
        return {
            'productId': int(product_id),
            'projectId': int(project_id),
            'skills': [item.to_dict() for item in skills],
            'rules': [item.to_dict() for item in rules],
            'skillTotal': len(skills),
            'ruleTotal': len(rules)
        }, ''

    @staticmethod
    def business_rule_list(session, req_data):
        filters = []
        project_id = SkillService._get(req_data, 'projectId', 'project_id')
        module_id = SkillService._get(req_data, 'moduleId', 'module_id')
        status = SkillService._get(req_data, 'status')
        priority = SkillService._get(req_data, 'priority')
        if project_id:
            filters.append(TestBusinessRule.project_id == int(project_id))
        if module_id not in (None, ''):
            filters.append(TestBusinessRule.module_id == int(module_id))
        if status not in (None, ''):
            filters.append(TestBusinessRule.status == int(status))
        if priority not in (None, ''):
            filters.append(TestBusinessRule.priority == int(priority))
        items, total = SkillDao.list_business_rule(
            session, filters,
            SkillService._get(req_data, 'pageNo', 'page', default=1),
            SkillService._get(req_data, 'pageSize', 'size', default=20),
            SkillService._get(req_data, 'keyword'),
            SkillService._get(req_data, 'tag')
        )
        return {'list': [item.to_dict() for item in items], 'total': total}
