# encoding: UTF-8
from datetime import date, datetime
from decimal import Decimal

from common.sqlSession import SqlSession


class BaseCrudController(object):
    """通用 Controller 基类，封装公共的请求取值与序列化逻辑。"""

    def __init__(self, req_data):
        # 每个 controller 持有一个独立 session，沿用当前项目的使用方式。
        self.session = SqlSession()
        # req_data 兼容 request.args 和 request.get_json() 两种来源。
        self.req_data = req_data

    def close_session(self):
        if self.session:
            self.session.close()

    @staticmethod
    def _get(req_data, *keys, default=None):
        """按顺序读取多个候选参数名，兼容前后端字段别名。"""
        for key in keys:
            value = req_data.get(key)
            if value not in (None, ''):
                return value
        return default

    @staticmethod
    def _format_value(value):
        """将数据库对象中的特殊类型转成可直接返回给前端的值。"""
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        if isinstance(value, Decimal):
            return float(value)
        return value

    @classmethod
    def serialize(cls, item, exclude=None):
        """单对象序列化，可按需排除不希望暴露给前端的字段。"""
        if not item:
            return {}
        exclude = exclude or []
        item_dict = item.to_dict()
        for key in exclude:
            item_dict.pop(key, None)
        for key, value in item_dict.items():
            item_dict[key] = cls._format_value(value)
        return item_dict

    @classmethod
    def serialize_list(cls, items, exclude=None):
        """列表对象序列化。"""
        return [cls.serialize(item, exclude) for item in items]
