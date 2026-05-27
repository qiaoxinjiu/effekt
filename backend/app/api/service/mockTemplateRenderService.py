# encoding: UTF-8
import json
import random
import re
import string
import uuid
from copy import deepcopy
from datetime import datetime

try:
    from faker import Faker
except Exception:
    Faker = None


class MockTemplateRenderService:
    PLACEHOLDER_RE = re.compile(r'^\{\{\s*([^{}]+?)\s*\}\}$')
    INLINE_PLACEHOLDER_RE = re.compile(r'\{\{\s*([^{}]+?)\s*\}\}')

    def __init__(self):
        self.faker = Faker('zh_CN') if Faker else None

    @staticmethod
    def json_loads(value, default=None):
        if value in (None, ''):
            return default
        if isinstance(value, (dict, list)):
            return value
        try:
            return json.loads(value)
        except Exception:
            return default

    @staticmethod
    def json_dumps(value):
        return json.dumps(value, ensure_ascii=False)

    def render(self, template, context):
        if isinstance(template, str):
            parsed = self.json_loads(template)
            if parsed is not None:
                return self.render(parsed, context)
            return self._render_string(template, context)
        if isinstance(template, list):
            return [self.render(item, context) for item in template]
        if isinstance(template, dict):
            return {key: self.render(value, context) for key, value in template.items()}
        return template

    def render_copy(self, template, context):
        return self.render(deepcopy(template), context)

    def _render_string(self, value, context):
        exact = self.PLACEHOLDER_RE.match(value)
        if exact:
            return self._resolve_expr(exact.group(1), context)
        return self.INLINE_PLACEHOLDER_RE.sub(lambda match: str(self._resolve_expr(match.group(1), context) or ''), value)

    def _resolve_expr(self, expr, context):
        expr = expr.strip()
        default = None
        if '|' in expr:
            expr, default = expr.split('|', 1)
            expr = expr.strip()
            default = self._coerce_literal(default.strip())
        value = self._resolve_without_default(expr, context)
        return default if value in (None, '') else value

    def _resolve_without_default(self, expr, context):
        if expr.startswith('request.'):
            return self._resolve_path(context, expr)
        if expr.startswith('faker.'):
            return self._resolve_faker(expr[6:])
        if expr == 'now':
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if expr == 'timestamp':
            return int(datetime.now().timestamp())
        if expr == 'uuid':
            return str(uuid.uuid4())
        if expr.startswith('random_int'):
            args = self._parse_args(expr)
            start = int(args[0]) if len(args) > 0 else 1
            end = int(args[1]) if len(args) > 1 else 999999
            return random.randint(start, end)
        if expr.startswith('random_string'):
            args = self._parse_args(expr)
            length = int(args[0]) if args else 16
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        if expr.startswith('scene.'):
            return self._resolve_path(context, expr)
        return None

    def _resolve_path(self, data, path):
        current = data
        for part in path.split('.'):
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        return current

    def _resolve_faker(self, expr):
        if not self.faker:
            return self._fallback_faker(expr)
        name = expr
        args = []
        if '(' in expr and expr.endswith(')'):
            name = expr[:expr.index('(')].strip()
            args = self._parse_args(expr)
        if name == 'integer':
            start = int(args[0]) if len(args) > 0 else 1
            end = int(args[1]) if len(args) > 1 else 999999
            return random.randint(start, end)
        method = getattr(self.faker, name, None)
        if callable(method):
            try:
                return method(*args)
            except Exception:
                return method()
        return self._fallback_faker(expr)

    def _fallback_faker(self, expr):
        if expr.startswith('phone'):
            return '13800138000'
        if expr.startswith('email'):
            return 'mock@example.com'
        if expr.startswith('name'):
            return '张三'
        if expr.startswith('address'):
            return '北京市朝阳区'
        return 'mock'

    def _parse_args(self, expr):
        if '(' not in expr or not expr.endswith(')'):
            return []
        raw = expr[expr.index('(') + 1:-1].strip()
        if not raw:
            return []
        return [self._coerce_literal(part.strip()) for part in raw.split(',')]

    @staticmethod
    def _coerce_literal(value):
        if value in ('true', 'True'):
            return True
        if value in ('false', 'False'):
            return False
        if value in ('null', 'None'):
            return None
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except Exception:
            return value
