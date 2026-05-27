# encoding: UTF-8
import random
import re
import string


class DataBuilderExecutor(object):
    """造数器同步执行器。

    当前版本只做安全的模板渲染和内置随机函数，不执行用户脚本，避免引入任意代码执行风险。
    """

    def __init__(self, builder_def, env=None):
        # builder_def 对应 data_builder.definition 字段，约定为 JSON 对象。
        self.builder_def = builder_def or {}
        # 保留 steps 字段，后续扩展 http/db 流程编排时继续复用。
        self.steps = self.builder_def.get('steps', [])
        self.env = env or {}
        # context 是模板变量来源，支持 {{env.xxx}} 和 {{param.xxx}}。
        self.context = {'env': self.env}
        self.results = []

    def execute(self, params=None):
        """执行造数器定义并返回渲染后的 output。"""
        params = params or {}
        self.context['param'] = params
        output = self.builder_def.get('output') or {}
        # 如果未配置 output，返回基础执行信息，方便前端判断定义是否为空。
        return self._render_template(output) if output else {'params': params, 'steps': len(self.steps)}

    def _render_template(self, obj):
        """递归渲染字符串、字典、数组中的 {{变量}}。"""
        if isinstance(obj, str):
            return re.sub(r'\{\{([^}]+)\}\}', lambda m: str(self._get_value(m.group(1).strip())), obj)
        if isinstance(obj, dict):
            return {k: self._render_template(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._render_template(item) for item in obj]
        return obj

    def _get_value(self, expr):
        """获取模板表达式的值，支持内置随机函数和点路径取值。"""
        if expr.startswith('random_string(') and expr.endswith(')'):
            length = int(expr[len('random_string('):-1] or 8)
            return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        if expr == 'random_phone()':
            return '1{}{}'.format(random.choice(['3', '5', '7', '8', '9']), ''.join(random.choice(string.digits) for _ in range(9)))
        current = self.context
        # 点路径示例：param.amount、env.base_url。
        for part in expr.split('.'):
            if isinstance(current, dict):
                current = current.get(part)
            else:
                current = getattr(current, part, None)
            if current is None:
                return ''
        return current
