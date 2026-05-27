# encoding: UTF-8


class MockStatusService:
    DOCUMENT_PARSE_STATUS = {
        0: '待解析',
        1: '解析成功',
        2: '解析失败',
        3: '部分成功'
    }

    INTERFACE_STATUS = {
        0: '草稿',
        1: '已启用',
        2: '已停用'
    }

    SCENE_STATUS = {
        0: '草稿',
        1: '已启用',
        2: '已停用'
    }

    ISSUE_STATUS = {
        0: '未处理',
        1: '已处理',
        2: '已忽略'
    }

    SOURCE_TYPE = {
        'openapi': 'OpenAPI / Swagger',
        'swagger': 'OpenAPI / Swagger',
        'apifox': 'Apifox',
        'yapi': 'YApi',
        'markdown': 'Markdown',
        'text': '文本文档',
        'pdf': 'PDF 文档',
        'word': 'Word 文档',
        'manual': '手动录入'
    }

    SCENE_CODE = {
        'success': '成功场景',
        'empty': '空数据场景',
        'error': '业务错误场景',
        'validation_error': '参数错误场景',
        'unauthorized': '未登录场景',
        'forbidden': '无权限场景',
        'server_error': '服务异常场景',
        'timeout': '超时场景',
        'custom': '自定义场景'
    }

    ISSUE_TYPE = {
        'json_invalid': 'JSON格式错误',
        'schema_incomplete': 'Schema不完整',
        'method_missing': '请求方法缺失',
        'path_missing': '接口路径缺失',
        'response_missing': '响应结构缺失',
        'ai_parse_failed': 'AI解析失败',
        'unsupported_format': '不支持的文档格式'
    }

    @staticmethod
    def get_text(mapping, value, default='未知'):
        try:
            if isinstance(value, str) and value.isdigit():
                value = int(value)
        except Exception:
            pass
        return mapping.get(value, default)

    @classmethod
    def append_document_text(cls, item):
        item['parse_status_text'] = cls.get_text(cls.DOCUMENT_PARSE_STATUS, item.get('parse_status'))
        item['source_type_text'] = cls.get_text(cls.SOURCE_TYPE, item.get('source_type'))
        return item

    @classmethod
    def append_interface_text(cls, item):
        item['status_text'] = cls.get_text(cls.INTERFACE_STATUS, item.get('status'))
        return item

    @classmethod
    def append_scene_text(cls, item):
        item['status_text'] = cls.get_text(cls.SCENE_STATUS, item.get('status'))
        item['scene_code_text'] = cls.get_text(cls.SCENE_CODE, item.get('scene_code'))
        return item

    @classmethod
    def append_issue_text(cls, item):
        item['status_text'] = cls.get_text(cls.ISSUE_STATUS, item.get('status'))
        item['issue_type_text'] = cls.get_text(cls.ISSUE_TYPE, item.get('issue_type'))
        return item
