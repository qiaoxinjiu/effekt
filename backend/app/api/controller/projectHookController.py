# encoding: UTF-8
import time
import hmac
import hashlib
import base64
import requests

from .baseCrudController import BaseCrudController
from ..model.projectHookModel import ProjectHook
from ..service.projectHookService import ProjectHookService


class ProjectHookController(BaseCrudController):
    def hook_list(self):
        filters = []
        project_id = self._get(self.req_data, 'projectId', 'project_id')
        hook_type = self._get(self.req_data, 'hookType', 'hook_type')

        if project_id:
            filters.append(ProjectHook.project_id == int(project_id))
        if hook_type not in (None, ''):
            filters.append(ProjectHook.hook_type == int(hook_type))

        items, total = ProjectHookService.list_by_filters(
            self.session, ProjectHook, filters,
            self._get(self.req_data, 'pageNo', 'page', default=1),
            self._get(self.req_data, 'pageSize', 'size', default=20),
            ProjectHook.created_time
        )

        result_list = []
        hook_type_map = {1: '飞书', 2: '钉钉', 3: '企微'}
        for item in items:
            hook_dict = item.to_dict()
            hook_dict['hook_type_name'] = hook_type_map.get(item.hook_type, '')
            result_list.append(hook_dict)

        return {'list': result_list, 'total': total}

    def hook_detail(self):
        hook_id = self._get(self.req_data, 'hookId', 'id')
        if not hook_id:
            return {}, 'hookId 为必传参数'
        item = ProjectHookService.get_by_id(self.session, ProjectHook, hook_id)
        if not item:
            return {}, '未查询到对应Hook配置！'
        ret = item.to_dict()
        hook_type_map = {1: '飞书', 2: '钉钉', 3: '企微'}
        ret['hook_type_name'] = hook_type_map.get(item.hook_type, '')
        return ret, ''

    def hook_create(self):
        project_id = self._get(self.req_data, 'projectId', 'project_id')
        hook_type = self._get(self.req_data, 'hookType', 'hook_type')
        webhook_url = self._get(self.req_data, 'webhookUrl', 'webhook_url')

        if not project_id:
            return 0, 'projectId 为必传参数'
        if not hook_type:
            return 0, 'hookType 为必传参数'
        if not webhook_url:
            return 0, 'webhookUrl 为必传参数'

        add_info = {
            'project_id': project_id,
            'hook_type': int(hook_type),
            'webhook_url': webhook_url,
            'secret': self._get(self.req_data, 'secret'),
            'enabled': int(self._get(self.req_data, 'enabled', default=1)),
            'description': self._get(self.req_data, 'description'),
            'config': self._get(self.req_data, 'config', default={}),
            'is_delete': 0
        }
        return ProjectHookService.create(self.session, ProjectHook, add_info)

    def hook_update(self):
        hook_id = self._get(self.req_data, 'hookId', 'id')
        if not hook_id:
            return 0, 'hookId 为必传参数'

        update_info = {}
        field_mapping = [
            (('hookType', 'hook_type'), 'hook_type'),
            (('webhookUrl', 'webhook_url'), 'webhook_url'),
            (('secret',), 'secret'),
            (('enabled',), 'enabled'),
            (('description',), 'description'),
            (('config',), 'config')
        ]

        for req_keys, column_key in field_mapping:
            value = self._get(self.req_data, *req_keys)
            if value is not None:
                update_info[column_key] = value

        return ProjectHookService.update_by_id(self.session, ProjectHook, hook_id, update_info)

    def hook_delete(self):
        hook_id = self._get(self.req_data, 'hookId', 'id')
        if not hook_id:
            return 0, 'hookId 为必传参数'
        return ProjectHookService.delete_by_id(self.session, ProjectHook, hook_id)

    def hook_send(self):
        project_id = self._get(self.req_data, 'projectId', 'project_id')
        title = self._get(self.req_data, 'title')
        content = self._get(self.req_data, 'content')
        hook_type = self._get(self.req_data, 'hookType', 'hook_type')
        hook_id = self._get(self.req_data, 'hookId', 'id')
        real_name = self._get(self.req_data, 'real_name', 'realName')

        if not project_id:
            return 0, 'projectId 为必传参数'
        if not title:
            return 0, 'title 为必传参数'
        if not content:
            return 0, 'content 为必传参数'

        at_prefix = f'@{real_name} ' if real_name else ''
        final_content = f'{at_prefix}{content}'

        if hook_id:
            hook = ProjectHookService.get_by_id(self.session, ProjectHook, hook_id)
            if not hook or hook.is_delete == 1 or hook.enabled != 1:
                return 0, '未找到对应的Hook或Hook未启用'
            hooks = [hook]
        else:
            hooks = ProjectHookService.get_hooks_by_project(self.session, project_id, hook_type)
            if not hooks:
                return 0, '未配置对应的Hook'

        results = []
        for hook in hooks:
            if hook.hook_type == 1:
                success, err_msg = self._send_feishu_message(hook.webhook_url, hook.secret, title, final_content)
            elif hook.hook_type == 2:
                success, err_msg = self._send_dingtalk_message(hook.webhook_url, hook.secret, title, final_content)
            elif hook.hook_type == 3:
                success, err_msg = self._send_wecom_message(hook.webhook_url, hook.secret, title, final_content)
            else:
                success, err_msg = False, '未知Hook类型'

            results.append({
                'hook_id': hook.id,
                'hook_type': hook.hook_type,
                'success': success,
                'error': err_msg
            })

        all_success = all(r['success'] for r in results)
        return 1 if all_success else 0, results

    def _send_feishu_message(self, webhook_url, secret, title, content):
        timestamp = str(int(time.time()))
        sign = ''
        if secret:
            string_to_sign = f'{timestamp}\n{secret}'
            hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).digest()
            sign = base64.b64encode(hmac_code).decode('utf-8')

        separator = '&' if '?' in webhook_url else '?'
        url = f'{webhook_url}{separator}timestamp={timestamp}&sign={sign}' if sign else webhook_url

        payload = {
            'msg_type': 'text',
            'content': {
                'text': f'【{title}】\n\n{content}'
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            if result.get('code') == 0:
                return True, ''
            else:
                return False, result.get('msg', '发送失败')
        except Exception as e:
            return False, str(e)

    def _send_dingtalk_message(self, webhook_url, secret, title, content):
        timestamp = str(int(time.time() * 1000))
        sign = ''
        if secret:
            string_to_sign = f'{timestamp}\n{secret}'
            hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).digest()
            sign = base64.b64encode(hmac_code).decode('utf-8')

        separator = '&' if '?' in webhook_url else '?'
        url = f'{webhook_url}{separator}timestamp={timestamp}&sign={sign}' if sign else webhook_url

        payload = {
            'msgtype': 'text',
            'text': {
                'content': f'【{title}】\n\n{content}'
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            if result.get('errcode') == 0:
                return True, ''
            else:
                return False, result.get('errmsg', '发送失败')
        except Exception as e:
            return False, str(e)

    def _send_wecom_message(self, webhook_url, secret, title, content):
        payload = {
            'msgtype': 'text',
            'text': {
                'content': f'【{title}】\n\n{content}'
            }
        }

        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            result = response.json()
            if result.get('errcode') == 0:
                return True, ''
            else:
                return False, result.get('errmsg', '发送失败')
        except Exception as e:
            return False, str(e)
