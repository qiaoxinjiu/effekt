# encoding: UTF-8
import copy
import json
import random

try:
    from faker import Faker
except Exception:
    Faker = None

from .aiService import AIService
from .mockTemplateRenderService import MockTemplateRenderService


class MockDataGeneratorService:
    def __init__(self):
        self.faker = Faker('zh_CN') if Faker else None

    def build_default_scenes(self, schema):
        request_example = self.generate_request_example(schema)
        response_template, ai_error = self.generate_response_template(schema)
        success_rule = self._build_pagination_rule(response_template)
        empty_template = copy.deepcopy(response_template)
        self._apply_empty_response(empty_template, success_rule)
        error_template = {'code': 40000, 'message': '业务处理失败', 'data': None}
        scenes = [
            {
                'scene_name': '成功场景',
                'scene_code': 'success',
                'http_status': 200,
                'delay_ms': 0,
                'request_example': request_example,
                'response_template': response_template,
                'response_headers': {'Content-Type': 'application/json', 'X-Mock-Scene': '{{scene.code}}'},
                'response_rule': success_rule,
                'match_rule': {},
                'priority': 0,
                'status': 0
            },
            {
                'scene_name': '空数据场景',
                'scene_code': 'empty',
                'http_status': 200,
                'delay_ms': 0,
                'request_example': request_example,
                'response_template': empty_template,
                'response_headers': {'Content-Type': 'application/json', 'X-Mock-Scene': '{{scene.code}}'},
                'response_rule': success_rule,
                'match_rule': {},
                'priority': 10,
                'status': 0
            },
            {
                'scene_name': '业务错误场景',
                'scene_code': 'error',
                'http_status': 200,
                'delay_ms': 0,
                'request_example': request_example,
                'response_template': error_template,
                'response_headers': {'Content-Type': 'application/json', 'X-Mock-Scene': '{{scene.code}}'},
                'response_rule': {},
                'match_rule': {},
                'priority': 20,
                'status': 0
            }
        ]
        return scenes, ai_error

    def generate_request_example(self, schema):
        result = {'headers': {}, 'query': {}, 'body': {}}
        for field in schema.get('headers') or []:
            result['headers'][field.get('name')] = self._value_for_field(field)
        for field in schema.get('query') or []:
            result['query'][field.get('name')] = self._value_for_field(field)
        body = schema.get('body') or {}
        result['body'] = self.generate_from_schema(body) if body else {}
        return result

    def generate_response_template(self, schema):
        response_schema = schema.get('response') or {}
        faker_template = self.generate_from_schema(response_schema, as_template=True)
        prompt = self._build_ai_prompt(schema, faker_template)
        ai_result, ai_error = AIService.request_json(prompt, 'AI生成Mock响应模板')
        if isinstance(ai_result, dict) and isinstance(ai_result.get('response_template'), dict):
            return ai_result['response_template'], ai_error
        if faker_template:
            return faker_template, ai_error
        return {'code': 20000, 'message': 'success', 'data': {}}, ai_error

    def generate_from_schema(self, schema, as_template=False):
        if not schema:
            return {}
        if isinstance(schema, list):
            return [self.generate_from_schema(schema[0], as_template)] if schema else []
        if isinstance(schema, dict) and 'properties' in schema:
            return {key: self.generate_from_schema(self._with_name(value, key), as_template) for key, value in (schema.get('properties') or {}).items()}
        if isinstance(schema, dict) and schema.get('type') == 'array':
            item = schema.get('items') or {'type': 'object', 'properties': {}}
            return [self.generate_from_schema(item, as_template)]
        if isinstance(schema, dict) and schema.get('type') == 'object':
            return {key: self.generate_from_schema(self._with_name(value, key), as_template) for key, value in (schema.get('properties') or {}).items()}
        return self._template_for_field(schema) if as_template else self._value_for_field(schema)

    @staticmethod
    def _with_name(value, name):
        if isinstance(value, dict):
            copied = dict(value)
            copied.setdefault('name', name)
            return copied
        return {'name': name, 'type': 'string'}

    def _value_for_field(self, field):
        if not isinstance(field, dict):
            return 'mock'
        if field.get('example') not in (None, ''):
            return field.get('example')
        enum_values = field.get('enum') or []
        if enum_values:
            return enum_values[0]
        name = str(field.get('name') or '').lower()
        field_type = str(field.get('type') or 'string').lower()
        if 'phone' in name or 'mobile' in name or '手机号' in str(field.get('description') or ''):
            return self.faker.phone_number() if self.faker else '13800138000'
        if 'email' in name or 'mail' in name:
            return self.faker.email() if self.faker else 'mock@example.com'
        if 'name' in name or '姓名' in str(field.get('description') or ''):
            return self.faker.name() if self.faker else '张三'
        if 'address' in name or '地址' in str(field.get('description') or ''):
            return self.faker.address() if self.faker else '北京市朝阳区'
        if 'time' in name or 'date' in name or '时间' in str(field.get('description') or ''):
            return '2026-01-01 10:00:00'
        if field_type in ('integer', 'int', 'long') or name.endswith('id') or name == 'id':
            return random.randint(1, 999999)
        if field_type in ('number', 'float', 'double', 'decimal'):
            return round(random.uniform(1, 9999), 2)
        if field_type in ('boolean', 'bool'):
            return True
        if field_type == 'array':
            return []
        if field_type == 'object':
            return {}
        return 'mock'

    def _template_for_field(self, field):
        if not isinstance(field, dict):
            return '{{faker.word}}'
        if field.get('example') not in (None, ''):
            return field.get('example')
        enum_values = field.get('enum') or []
        if enum_values:
            return enum_values[0]
        name = str(field.get('name') or '').lower()
        desc = str(field.get('description') or '')
        field_type = str(field.get('type') or 'string').lower()
        if 'phone' in name or 'mobile' in name or '手机号' in desc:
            return '{{faker.phone_number}}'
        if 'email' in name or 'mail' in name:
            return '{{faker.email}}'
        if 'name' in name or '姓名' in desc:
            return '{{faker.name}}'
        if 'address' in name or '地址' in desc:
            return '{{faker.address}}'
        if 'time' in name or 'date' in name or '时间' in desc:
            return '{{now}}'
        if field_type in ('integer', 'int', 'long') or name.endswith('id') or name == 'id':
            return '{{faker.integer(1,999999)}}'
        if field_type in ('number', 'float', 'double', 'decimal'):
            return '{{faker.pyfloat}}'
        if field_type in ('boolean', 'bool'):
            return True
        return '{{faker.word}}'

    def _build_ai_prompt(self, schema, faker_template):
        return f'''你是接口Mock数据生成助手。请基于接口定义和Faker模板生成更符合字段语义的响应模板。
要求：
1. 只输出JSON对象，不输出Markdown。
2. JSON结构固定为：{{"response_template": {{...}}}}
3. 动态字段使用占位符：{{{{faker.name}}}}、{{{{faker.phone_number}}}}、{{{{faker.email}}}}、{{{{faker.integer(1,999999)}}}}、{{{{now}}}}。
4. 详情ID可使用请求引用：{{{{request.query.id|10001}}}} 或 {{{{request.path.id|10001}}}}。
5. 不要改变原响应结构。

接口定义：
{json.dumps(schema, ensure_ascii=False)}

Faker基础模板：
{json.dumps(faker_template, ensure_ascii=False)}
'''

    def _build_pagination_rule(self, response_template):
        list_path = self._find_list_path(response_template)
        if not list_path:
            return {}
        item_template = self._get_by_path(response_template, list_path)
        if isinstance(item_template, list) and item_template:
            item_template = item_template[0]
        else:
            item_template = {}
        prefix = '.'.join(list_path.split('.')[:-1])
        return {
            'pagination': {
                'enabled': True,
                'listPath': list_path,
                'itemTemplate': item_template,
                'pageNoParam': 'pageNo',
                'pageSizeParam': 'pageSize',
                'defaultPageNo': 1,
                'defaultPageSize': 10,
                'maxPageSize': 100,
                'total': '{{faker.integer(50,500)}}',
                'pageNoPath': f'{prefix}.pageNo' if prefix else 'pageNo',
                'pageSizePath': f'{prefix}.pageSize' if prefix else 'pageSize',
                'totalPath': f'{prefix}.total' if prefix else 'total'
            }
        }

    def _find_list_path(self, value, prefix=''):
        if isinstance(value, dict):
            for key, item in value.items():
                current = f'{prefix}.{key}' if prefix else key
                if key in ('list', 'records', 'items', 'rows') and isinstance(item, list):
                    return current
                found = self._find_list_path(item, current)
                if found:
                    return found
        if isinstance(value, list) and value:
            return self._find_list_path(value[0], prefix)
        return None

    def _get_by_path(self, data, path):
        current = data
        for part in path.split('.'):
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        return current

    def _apply_empty_response(self, template, rule):
        pagination = (rule or {}).get('pagination') or {}
        if pagination.get('listPath'):
            self._set_by_path(template, pagination['listPath'], [])
        if pagination.get('totalPath'):
            self._set_by_path(template, pagination['totalPath'], 0)

    def _set_by_path(self, data, path, value):
        current = data
        parts = path.split('.')
        for part in parts[:-1]:
            if not isinstance(current, dict):
                return
            current = current.setdefault(part, {})
        if isinstance(current, dict):
            current[parts[-1]] = value
