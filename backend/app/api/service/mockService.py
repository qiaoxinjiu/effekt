# encoding: UTF-8
import json
import os
import re
import time
from datetime import datetime
import requests

from ..dao.mockDao import MockDao
from ..model.mockModel import MockDocument, MockInterface, MockScene, MockCallLog, MockParseIssue
from .mockDataGeneratorService import MockDataGeneratorService
from .mockMatchService import MockMatchService
from .mockParserService import MockParserService
from .mockTemplateRenderService import MockTemplateRenderService


class MockService:
    ATTACHMENT_DIR = os.path.join(os.getcwd(), 'attachment', 'interface_address')

    @staticmethod
    def upload_import_document(session, form_data, files):
        product_id = form_data.get('productId') or form_data.get('product_id')
        project_id = form_data.get('projectId') or form_data.get('project_id')
        name = form_data.get('name') or form_data.get('documentName') or form_data.get('document_name') or 'Mock接口文档'
        source_type = (form_data.get('sourceType') or form_data.get('source_type') or '').lower()
        created_by = form_data.get('createdBy') or form_data.get('created_by')
        upload_file = files.get('file') if files else None
        if not product_id or not project_id:
            return {}, 'productId、projectId 为必传参数'
        if not upload_file or not upload_file.filename:
            return {}, 'file 为必传参数'
        file_path, file_name = MockService._save_upload_file(upload_file, name)
        detected_type = source_type or MockService._detect_source_type(file_name)
        content = MockService._read_file_content(file_path, detected_type)
        req_data = {
            'productId': product_id,
            'projectId': project_id,
            'name': name,
            'sourceType': detected_type,
            'source': file_path,
            'content': content,
            'createdBy': created_by
        }
        ret, err_msg = MockService.import_document(session, req_data)
        if err_msg:
            return ret, err_msg
        ret.update({'filePath': file_path, 'fileName': file_name, 'sourceType': detected_type})
        return ret, ''

    @staticmethod
    def url_import_document(session, req_data):
        product_id = req_data.get('productId') or req_data.get('product_id')
        project_id = req_data.get('projectId') or req_data.get('project_id')
        name = req_data.get('name') or req_data.get('documentName') or 'Mock接口文档'
        source_type = (req_data.get('sourceType') or req_data.get('source_type') or 'openapi').lower()
        source_url = req_data.get('url') or req_data.get('source')
        created_by = req_data.get('createdBy') or req_data.get('created_by')
        if not product_id or not project_id:
            return {}, 'productId、projectId 为必传参数'
        if not source_url:
            return {}, 'url 为必传参数'
        content, fetch_error = MockService._fetch_url_content(source_url)
        if fetch_error:
            return {}, fetch_error
        return MockService.import_document(session, {
            'productId': product_id,
            'projectId': project_id,
            'name': name,
            'sourceType': source_type,
            'source': source_url,
            'content': content,
            'createdBy': created_by
        })

    @staticmethod
    def import_document(session, req_data):
        product_id = req_data.get('productId') or req_data.get('product_id')
        project_id = req_data.get('projectId') or req_data.get('project_id')
        name = req_data.get('name') or 'Mock接口文档'
        source_type = (req_data.get('sourceType') or req_data.get('source_type') or 'manual').lower()
        source = req_data.get('source')
        content = req_data.get('content') or req_data.get('schema') or ''
        created_by = req_data.get('createdBy') or req_data.get('created_by')
        if not product_id or not project_id:
            return {}, 'productId、projectId 为必传参数'
        document = MockDocument(
            product_id=product_id,
            project_id=project_id,
            name=name,
            source_type=source_type,
            source=source,
            content=content if isinstance(content, str) else json.dumps(content, ensure_ascii=False),
            parse_status=0,
            created_by=created_by,
            is_delete=0
        )
        document_id = MockDao.create(session, document)
        interfaces, issues = MockParserService.parse(source_type, content, source)
        generator = MockDataGeneratorService()
        interface_ids = []
        for schema in interfaces:
            path_regex, path_params, path_score = MockMatchService.build_path_pattern(schema.get('path'))
            interface = MockInterface(
                document_id=document_id,
                product_id=product_id,
                project_id=project_id,
                name=schema.get('name') or f"{schema.get('method')} {schema.get('path')}",
                path=MockMatchService.normalize_path(schema.get('path')),
                method=str(schema.get('method') or 'GET').upper(),
                description=schema.get('description') or '',
                headers_schema=json.dumps(schema.get('headers') or [], ensure_ascii=False),
                query_schema=json.dumps(schema.get('query') or [], ensure_ascii=False),
                body_schema=json.dumps(schema.get('body') or {}, ensure_ascii=False),
                response_schema=json.dumps(schema.get('response') or {}, ensure_ascii=False),
                raw_schema=json.dumps(schema, ensure_ascii=False),
                path_regex=path_regex,
                path_params=json.dumps(path_params, ensure_ascii=False),
                path_score=path_score,
                status=0,
                created_by=created_by,
                is_delete=0
            )
            interface_id = MockDao.create(session, interface)
            interface_ids.append(interface_id)
            scenes, ai_error = generator.build_default_scenes(schema)
            if ai_error:
                issues.append({'issue_type': 'ai_parse_failed', 'source_fragment': schema.get('path'), 'error_message': ai_error, 'suggestion': '已使用Faker兜底生成响应模板，请人工确认'})
            for scene in scenes:
                MockDao.create(session, MockScene(
                    interface_id=interface_id,
                    scene_name=scene['scene_name'],
                    scene_code=scene['scene_code'],
                    http_status=scene['http_status'],
                    delay_ms=scene['delay_ms'],
                    request_example=json.dumps(scene['request_example'], ensure_ascii=False),
                    response_template=json.dumps(scene['response_template'], ensure_ascii=False),
                    response_headers=json.dumps(scene['response_headers'], ensure_ascii=False),
                    response_rule=json.dumps(scene['response_rule'], ensure_ascii=False),
                    match_rule=json.dumps(scene['match_rule'], ensure_ascii=False),
                    priority=scene['priority'],
                    status=scene['status'],
                    is_delete=0
                ))
        for issue in issues:
            MockDao.create(session, MockParseIssue(
                document_id=document_id,
                issue_type=issue.get('issue_type') or 'schema_incomplete',
                source_fragment=issue.get('source_fragment'),
                error_message=issue.get('error_message'),
                suggestion=issue.get('suggestion'),
                status=0
            ))
        parse_status = 1 if interfaces and not issues else 3 if interfaces and issues else 2
        MockDao.update_by_id(session, MockDocument, document_id, {
            'parse_status': parse_status,
            'parse_error': '' if interfaces else (issues[0].get('error_message') if issues else '未解析到接口'),
            'interface_count': len(interfaces)
        })
        session.commit()
        return {'documentId': document_id, 'interfaceIds': interface_ids, 'interfaceCount': len(interfaces), 'issueCount': len(issues), 'parseStatus': parse_status}, ''

    @staticmethod
    def list_documents(session, req_data):
        filters = [MockDocument.is_delete == 0]
        project_id = req_data.get('projectId') or req_data.get('project_id')
        if project_id:
            filters.append(MockDocument.project_id == project_id)
        page_no, page_size = MockService._page(req_data)
        return MockDao.list_by_filters(session, MockDocument, filters, page_no, page_size, MockDocument.created_time.desc())

    @staticmethod
    def list_interfaces(session, req_data):
        filters = [MockInterface.is_delete == 0]
        for req_key, column in [('projectId', MockInterface.project_id), ('documentId', MockInterface.document_id), ('status', MockInterface.status)]:
            value = req_data.get(req_key) or req_data.get(MockService._camel_to_snake(req_key))
            if value not in (None, ''):
                filters.append(column == value)
        keyword = req_data.get('keyword')
        if keyword:
            filters.append(MockInterface.name.like(f'%{keyword}%'))
        page_no, page_size = MockService._page(req_data)
        return MockDao.list_by_filters(session, MockInterface, filters, page_no, page_size, MockInterface.created_time.desc())

    @staticmethod
    def get_interface(session, interface_id):
        return MockDao.get_by_id(session, MockInterface, interface_id)

    @staticmethod
    def update_interface(session, interface_id, req_data):
        allowed = ['name', 'path', 'method', 'description', 'headers_schema', 'query_schema', 'body_schema', 'response_schema', 'raw_schema']
        update_info = {}
        for field in allowed:
            value = req_data.get(field) or req_data.get(MockService._snake_to_camel(field))
            if value is not None:
                update_info[field] = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        if 'path' in update_info:
            regex, params, score = MockMatchService.build_path_pattern(update_info['path'])
            update_info['path'] = MockMatchService.normalize_path(update_info['path'])
            update_info['path_regex'] = regex
            update_info['path_params'] = json.dumps(params, ensure_ascii=False)
            update_info['path_score'] = score
        return MockDao.update_by_id(session, MockInterface, interface_id, update_info)

    @staticmethod
    def set_interface_status(session, interface_id, status):
        return MockDao.update_by_id(session, MockInterface, interface_id, {'status': status})

    @staticmethod
    def list_scenes(session, req_data):
        interface_id = req_data.get('interfaceId') or req_data.get('interface_id')
        if not interface_id:
            return [], 0
        scenes = MockDao.list_scenes(session, interface_id)
        return scenes, len(scenes)

    @staticmethod
    def update_scene(session, scene_id, req_data):
        allowed = ['scene_name', 'scene_code', 'http_status', 'delay_ms', 'request_example', 'response_template', 'response_headers', 'response_rule', 'match_rule', 'priority']
        update_info = {}
        for field in allowed:
            value = req_data.get(field) or req_data.get(MockService._snake_to_camel(field))
            if value is not None:
                update_info[field] = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        return MockDao.update_by_id(session, MockScene, scene_id, update_info)

    @staticmethod
    def set_scene_status(session, scene_id, status):
        return MockDao.update_by_id(session, MockScene, scene_id, {'status': status})

    @staticmethod
    def list_logs(session, req_data):
        filters = []
        project_id = req_data.get('projectId') or req_data.get('project_id')
        interface_id = req_data.get('interfaceId') or req_data.get('interface_id')
        if project_id:
            filters.append(MockCallLog.project_id == project_id)
        if interface_id:
            filters.append(MockCallLog.interface_id == interface_id)
        page_no, page_size = MockService._page(req_data)
        return MockDao.list_by_filters(session, MockCallLog, filters, page_no, page_size, MockCallLog.created_time.desc())

    @staticmethod
    def list_issues(session, req_data):
        filters = []
        document_id = req_data.get('documentId') or req_data.get('document_id')
        if document_id:
            filters.append(MockParseIssue.document_id == document_id)
        page_no, page_size = MockService._page(req_data)
        return MockDao.list_by_filters(session, MockParseIssue, filters, page_no, page_size, MockParseIssue.created_time.desc())

    @staticmethod
    def runtime(session, method, path, query, body, headers):
        started = time.time()
        renderer = MockTemplateRenderService()
        project_id = query.get('projectId') or query.get('project_id')
        if not project_id:
            return {'success': False, 'code': 40000, 'message': 'projectId 为必传参数'}, 400, {}, 'projectId 为必传参数'
        normalized_path = MockMatchService.normalize_path(path)
        interfaces = MockDao.find_enabled_interfaces(session, project_id, method)
        interface, path_params = MockMatchService.match_interface(interfaces, normalized_path)
        if not interface:
            return {'success': False, 'code': 40400, 'message': '未匹配到启用的Mock接口'}, 404, {}, '未匹配到启用的Mock接口'
        scenes = MockDao.list_scenes(session, interface.id, only_enabled=True)
        business_query = {k: v for k, v in query.items() if k not in ('projectId', 'project_id', 'mockScene')}
        context = {'request': {'query': business_query, 'body': body or {}, 'headers': headers or {}, 'path': path_params}, 'scene': {}}
        scene = MockMatchService.choose_scene(scenes, query.get('mockScene'), context)
        if not scene:
            return {'success': False, 'code': 40401, 'message': '未匹配到启用的Mock场景'}, 404, {}, '未匹配到启用的Mock场景'
        context['scene'] = {'code': scene.scene_code, 'name': scene.scene_name, 'id': scene.id}
        template = renderer.json_loads(scene.response_template, {})
        response_body = renderer.render_copy(template, context)
        rule = renderer.json_loads(scene.response_rule, {})
        MockService._apply_pagination(response_body, rule, context, renderer, scene.scene_code)
        response_headers = renderer.render_copy(renderer.json_loads(scene.response_headers, {'Content-Type': 'application/json'}), context)
        delay_ms = scene.delay_ms or 0
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)
        http_status = scene.http_status or 200
        duration_ms = int((time.time() - started) * 1000)
        MockDao.create(session, MockCallLog(
            project_id=project_id,
            interface_id=interface.id,
            scene_id=scene.id,
            method=method.upper(),
            path=normalized_path,
            request_query=json.dumps(business_query, ensure_ascii=False),
            request_body=json.dumps(body or {}, ensure_ascii=False),
            response_body=json.dumps(response_body, ensure_ascii=False),
            http_status=http_status,
            duration_ms=duration_ms
        ))
        session.commit()
        return response_body, http_status, response_headers, ''

    @staticmethod
    def _apply_pagination(response_body, rule, context, renderer, scene_code):
        pagination = (rule or {}).get('pagination') or {}
        if not pagination.get('enabled'):
            return
        query = context.get('request', {}).get('query', {}) or {}
        page_size = MockService._to_int(query.get(pagination.get('pageSizeParam') or 'pageSize'), pagination.get('defaultPageSize') or 10)
        page_no = MockService._to_int(query.get(pagination.get('pageNoParam') or 'pageNo'), pagination.get('defaultPageNo') or 1)
        max_page_size = pagination.get('maxPageSize') or 100
        page_size = min(max(page_size, 0), max_page_size)
        if scene_code == 'empty':
            items, total = [], 0
        else:
            item_template = pagination.get('itemTemplate') or {}
            items = [renderer.render_copy(item_template, context) for _ in range(page_size)]
            total = renderer.render(pagination.get('total') or '{{faker.integer(50,500)}}', context)
        MockService._set_by_path(response_body, pagination.get('listPath'), items)
        MockService._set_by_path(response_body, pagination.get('totalPath'), total)
        MockService._set_by_path(response_body, pagination.get('pageNoPath'), page_no)
        MockService._set_by_path(response_body, pagination.get('pageSizePath'), page_size)

    @staticmethod
    def _set_by_path(data, path, value):
        if not path:
            return
        current = data
        parts = path.split('.')
        for part in parts[:-1]:
            if not isinstance(current, dict):
                return
            current = current.setdefault(part, {})
        if isinstance(current, dict):
            current[parts[-1]] = value

    @staticmethod
    def _page(req_data):
        return int(req_data.get('pageNo', req_data.get('page', 1))), int(req_data.get('pageSize', req_data.get('size', 20)))

    @staticmethod
    def _to_int(value, default):
        try:
            return int(value)
        except Exception:
            return int(default)

    @staticmethod
    def _snake_to_camel(value):
        parts = value.split('_')
        return parts[0] + ''.join(part.capitalize() for part in parts[1:])

    @staticmethod
    def _camel_to_snake(value):
        chars = []
        for char in value:
            if char.isupper():
                chars.append('_')
                chars.append(char.lower())
            else:
                chars.append(char)
        return ''.join(chars).lstrip('_')

    @staticmethod
    def _fetch_url_content(source_url):
        if re.match(r'^https?://app\.apifox\.com/project/\d+', source_url or ''):
            return None, '当前填写的是 Apifox 项目页面地址，不是可直接拉取的接口文档 JSON。请在 Apifox 中导出 OpenAPI/Swagger JSON 文件后上传，或填写可公开访问的 OpenAPI JSON 地址。'
        headers = {
            'Accept': 'application/json,text/plain,*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
        }
        try:
            response = requests.get(source_url, headers=headers, timeout=30)
        except requests.exceptions.SSLError:
            try:
                response = requests.get(source_url, headers=headers, timeout=30, verify=False)
            except Exception as e:
                return None, f'拉取接口文档失败：HTTPS 连接失败。请确认 URL 是可直接访问的接口文档 JSON 地址，或改为上传导出的 JSON 文件。错误：{str(e)}'
        except Exception as e:
            return None, f'拉取接口文档失败：{str(e)}'
        try:
            response.raise_for_status()
        except Exception as e:
            return None, f'拉取接口文档失败：HTTP {response.status_code}。请确认文档地址可公开访问且不需要登录。错误：{str(e)}'
        content_type = response.headers.get('Content-Type', '')
        text = response.text
        if 'text/html' in content_type.lower() or '<html' in text[:500].lower():
            return None, '拉取到的是 HTML 页面，不是接口文档 JSON。请填写 Swagger/OpenAPI/YApi/Apifox 的 JSON 导出地址，或直接上传导出的 JSON 文件。'
        if 'json' in content_type.lower() or text.strip().startswith(('{', '[')):
            try:
                return response.json(), ''
            except Exception:
                return text, ''
        return text, ''

    @staticmethod
    def _save_upload_file(upload_file, document_name):
        os.makedirs(MockService.ATTACHMENT_DIR, exist_ok=True)
        original = upload_file.filename or 'interface_document'
        _, ext = os.path.splitext(original)
        safe_name = re.sub(r'[\\/:*?"<>|\s]+', '_', str(document_name or '').strip()).strip('_') or 'interface_document'
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        file_name = f'{safe_name}_{timestamp}{ext.lower()}'
        file_path = os.path.join(MockService.ATTACHMENT_DIR, file_name)
        upload_file.save(file_path)
        return file_path, file_name

    @staticmethod
    def _detect_source_type(file_name):
        ext = os.path.splitext(file_name or '')[1].lower()
        if ext == '.json':
            return 'openapi'
        if ext in ('.md', '.markdown'):
            return 'markdown'
        if ext == '.txt':
            return 'text'
        if ext == '.pdf':
            return 'pdf'
        if ext in ('.doc', '.docx'):
            return 'word'
        return 'text'

    @staticmethod
    def _read_file_content(file_path, source_type):
        if source_type in ('pdf', 'word'):
            return file_path
        for encoding in ('utf-8-sig', 'utf-8', 'gbk'):
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    text = f.read()
                if source_type in ('openapi', 'swagger', 'apifox', 'yapi'):
                    try:
                        return json.loads(text)
                    except Exception:
                        return text
                return text
            except UnicodeDecodeError:
                continue
        with open(file_path, 'rb') as f:
            return f.read().decode('utf-8', errors='ignore')
