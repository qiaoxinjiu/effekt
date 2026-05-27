# encoding: UTF-8
import json
import os
import re
import zipfile
import xml.etree.ElementTree as ET

from .aiService import AIService


class MockParserService:
    @staticmethod
    def parse(source_type, content, source=None):
        source_type = (source_type or 'manual').lower()
        if source_type in ('manual',):
            return MockParserService._parse_manual(content)
        if source_type in ('openapi', 'swagger', 'apifox'):
            return MockParserService._parse_openapi(content)
        if source_type == 'yapi':
            return MockParserService._parse_yapi(content)
        if source_type in ('markdown', 'text', 'pdf', 'word'):
            text, err = MockParserService._extract_text(source_type, content, source)
            if err:
                return [], [{'issue_type': 'unsupported_format', 'source_fragment': source or '', 'error_message': err, 'suggestion': '请检查文档格式或改为手动录入'}]
            return MockParserService._parse_text_by_ai(text)
        return [], [{'issue_type': 'unsupported_format', 'source_fragment': source_type, 'error_message': '不支持的文档格式', 'suggestion': '请选择支持的sourceType'}]

    @staticmethod
    def _parse_manual(content):
        data = MockParserService._loads(content)
        if isinstance(data, dict) and 'interfaces' in data:
            interfaces = data.get('interfaces') or []
        elif isinstance(data, list):
            interfaces = data
        elif isinstance(data, dict):
            interfaces = [data]
        else:
            return [], [{'issue_type': 'json_invalid', 'source_fragment': str(content)[:500], 'error_message': 'manual内容不是合法JSON', 'suggestion': '请传入接口Schema或interfaces数组'}]
        return MockParserService._normalize_interfaces(interfaces), []

    @staticmethod
    def _parse_openapi(content):
        data = MockParserService._loads(content)
        if not isinstance(data, dict):
            return [], [{'issue_type': 'json_invalid', 'source_fragment': str(content)[:500], 'error_message': 'OpenAPI内容不是合法JSON', 'suggestion': '请检查导出内容'}]
        paths = data.get('paths') or {}
        components = data.get('components', {}).get('schemas', {}) or data.get('definitions', {}) or {}
        interfaces = []
        issues = []
        for path, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            for method, operation in path_item.items():
                if method.lower() not in ('get', 'post', 'put', 'delete', 'patch', 'options', 'head'):
                    continue
                try:
                    interfaces.append(MockParserService._normalize_openapi_operation(path, method, operation or {}, components))
                except Exception as e:
                    issues.append({'issue_type': 'schema_incomplete', 'source_fragment': path, 'error_message': str(e), 'suggestion': '请手动补录该接口'})
        return interfaces, issues

    @staticmethod
    def _normalize_openapi_operation(path, method, operation, components):
        parameters = operation.get('parameters') or []
        headers = []
        query = []
        for param in parameters:
            schema = MockParserService._resolve_ref(param.get('schema') or {}, components)
            field = {
                'name': param.get('name'),
                'type': schema.get('type') or 'string',
                'required': param.get('required', False),
                'description': param.get('description') or '',
                'example': param.get('example') or schema.get('example'),
                'enum': schema.get('enum') or []
            }
            if param.get('in') == 'header':
                headers.append(field)
            else:
                query.append(field)
        body_schema = {}
        request_body = operation.get('requestBody') or {}
        content = request_body.get('content') or {}
        if content:
            media = content.get('application/json') or next(iter(content.values()))
            body_schema = MockParserService._schema_to_simple(MockParserService._resolve_ref(media.get('schema') or {}, components), components)
        response_schema = {}
        responses = operation.get('responses') or {}
        response_obj = responses.get('200') or responses.get(200) or responses.get('default') or {}
        response_content = response_obj.get('content') or {}
        if response_content:
            media = response_content.get('application/json') or next(iter(response_content.values()))
            response_schema = MockParserService._schema_to_simple(MockParserService._resolve_ref(media.get('schema') or {}, components), components)
        return {
            'name': operation.get('summary') or operation.get('operationId') or f'{method.upper()} {path}',
            'path': path,
            'method': method.upper(),
            'description': operation.get('description') or '',
            'headers': headers,
            'query': query,
            'body': body_schema,
            'response': response_schema,
            'sourceType': 'openapi',
            'raw': operation
        }

    @staticmethod
    def _parse_yapi(content):
        data = MockParserService._loads(content)
        if not isinstance(data, (dict, list)):
            return [], [{'issue_type': 'json_invalid', 'source_fragment': str(content)[:500], 'error_message': 'YApi内容不是合法JSON', 'suggestion': '请检查导出内容'}]
        records = data if isinstance(data, list) else data.get('list') or data.get('interfaces') or data.get('api') or []
        interfaces = []
        for item in records:
            if not isinstance(item, dict):
                continue
            res_body = MockParserService._loads(item.get('res_body'), {})
            req_body = MockParserService._loads(item.get('req_body_other'), {})
            query = []
            for param in item.get('req_query') or []:
                query.append({'name': param.get('name'), 'type': param.get('type') or 'string', 'required': str(param.get('required')) == '1', 'description': param.get('desc') or ''})
            interfaces.append({
                'name': item.get('title') or item.get('name') or item.get('path'),
                'path': item.get('path'),
                'method': str(item.get('method') or 'GET').upper(),
                'description': item.get('desc') or '',
                'headers': [],
                'query': query,
                'body': MockParserService._json_to_schema(req_body),
                'response': MockParserService._json_to_schema(res_body),
                'sourceType': 'yapi',
                'raw': item
            })
        return MockParserService._normalize_interfaces(interfaces), []

    @staticmethod
    def _parse_text_by_ai(text):
        prompt = f'''请从下面接口文档中提取接口定义，输出严格JSON对象，不要Markdown。
输出格式：{{"interfaces":[{{"name":"","path":"/api/demo","method":"GET","description":"","headers":[],"query":[],"body":{{}},"response":{{}}}}]}}
字段schema使用JSON Schema简化结构：type/properties/items/description/example/enum。
接口文档：
{text[:20000]}
'''
        result, err = AIService.request_json(prompt, 'AI解析Mock接口文档')
        if err:
            return [], [{'issue_type': 'ai_parse_failed', 'source_fragment': text[:1000], 'error_message': err, 'suggestion': '请手动补录或调整文档格式'}]
        interfaces = result.get('interfaces') if isinstance(result, dict) else result
        return MockParserService._normalize_interfaces(interfaces or []), []

    @staticmethod
    def _extract_text(source_type, content, source):
        if source_type in ('markdown', 'text'):
            return content or '', ''
        file_path = source or content
        if not file_path or not os.path.exists(file_path):
            return '', '文件不存在'
        try:
            if source_type == 'pdf':
                try:
                    import pdfplumber
                    texts = []
                    with pdfplumber.open(file_path) as pdf:
                        for page in pdf.pages:
                            texts.append(page.extract_text() or '')
                    return '\n'.join(texts), ''
                except Exception:
                    from PyPDF2 import PdfReader
                    reader = PdfReader(file_path)
                    return '\n'.join([page.extract_text() or '' for page in reader.pages]), ''
            if source_type == 'word':
                if file_path.lower().endswith('.docx'):
                    return MockParserService._extract_docx_text(file_path), ''
                return '', '暂不支持 .doc 老格式，请另存为 .docx 后上传'
        except Exception as e:
            return '', str(e)
        return '', '不支持的文档格式'

    @staticmethod
    def _extract_docx_text(file_path):
        texts = []
        with zipfile.ZipFile(file_path) as docx_zip:
            with docx_zip.open('word/document.xml') as document_xml:
                tree = ET.parse(document_xml)
        namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        for paragraph in tree.findall('.//w:p', namespace):
            paragraph_text = ''.join(node.text or '' for node in paragraph.findall('.//w:t', namespace))
            if paragraph_text:
                texts.append(paragraph_text)
        return '\n'.join(texts)

    @staticmethod
    def _normalize_interfaces(interfaces):
        result = []
        for item in interfaces or []:
            if not isinstance(item, dict) or not item.get('path') or not item.get('method'):
                continue
            result.append({
                'name': item.get('name') or item.get('title') or f"{str(item.get('method')).upper()} {item.get('path')}",
                'path': item.get('path'),
                'method': str(item.get('method')).upper(),
                'description': item.get('description') or item.get('desc') or '',
                'headers': item.get('headers') or [],
                'query': item.get('query') or item.get('parameters') or [],
                'body': item.get('body') or {},
                'response': item.get('response') or {},
                'sourceType': item.get('sourceType') or item.get('source_type') or 'manual',
                'raw': item.get('raw') or item
            })
        return result

    @staticmethod
    def _schema_to_simple(schema, components):
        schema = MockParserService._resolve_ref(schema or {}, components)
        if not isinstance(schema, dict):
            return {}
        if schema.get('type') == 'array':
            return {'type': 'array', 'items': MockParserService._schema_to_simple(schema.get('items') or {}, components)}
        properties = schema.get('properties') or {}
        if properties:
            return {'type': 'object', 'properties': {key: MockParserService._schema_to_simple(value, components) for key, value in properties.items()}, 'description': schema.get('description') or ''}
        return {'type': schema.get('type') or 'string', 'description': schema.get('description') or '', 'example': schema.get('example'), 'enum': schema.get('enum') or []}

    @staticmethod
    def _json_to_schema(value):
        if isinstance(value, dict):
            return {'type': 'object', 'properties': {key: MockParserService._json_to_schema(val) for key, val in value.items()}}
        if isinstance(value, list):
            return {'type': 'array', 'items': MockParserService._json_to_schema(value[0]) if value else {'type': 'object', 'properties': {}}}
        if isinstance(value, bool):
            return {'type': 'boolean'}
        if isinstance(value, int):
            return {'type': 'integer'}
        if isinstance(value, float):
            return {'type': 'number'}
        return {'type': 'string'}

    @staticmethod
    def _resolve_ref(schema, components):
        if not isinstance(schema, dict):
            return schema
        ref = schema.get('$ref')
        if ref:
            name = ref.split('/')[-1]
            return components.get(name) or schema
        return schema

    @staticmethod
    def _loads(value, default=None):
        if value in (None, ''):
            return default
        if isinstance(value, (dict, list)):
            return value
        try:
            return json.loads(value)
        except Exception:
            return default
