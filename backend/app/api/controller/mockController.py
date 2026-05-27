# encoding: UTF-8
from flask import make_response

from .baseCrudController import BaseCrudController
from ..model.mockModel import MockDocument, MockInterface, MockScene, MockParseIssue
from ..service.mockService import MockService
from ..service.mockStatusService import MockStatusService


class MockController(BaseCrudController):
    def document_import(self):
        return MockService.import_document(self.session, self.req_data)

    def document_upload_import(self):
        return MockService.upload_import_document(self.session, self.req_data.form, self.req_data.files)

    def document_url_import(self):
        return MockService.url_import_document(self.session, self.req_data)

    def document_list(self):
        items, total = MockService.list_documents(self.session, self.req_data)
        data = [MockStatusService.append_document_text(self.serialize(item, ['is_delete'])) for item in items]
        return {'list': data, 'total': total}

    def interface_list(self):
        items, total = MockService.list_interfaces(self.session, self.req_data)
        data = [MockStatusService.append_interface_text(self.serialize(item, ['is_delete'])) for item in items]
        return {'list': data, 'total': total}

    def interface_detail(self):
        interface_id = self._get(self.req_data, 'interfaceId', 'interface_id', 'id')
        if not interface_id:
            return {}, 'interfaceId 为必传参数'
        item = MockService.get_interface(self.session, interface_id)
        if not item:
            return {}, 'Mock接口不存在'
        return MockStatusService.append_interface_text(self.serialize(item, ['is_delete'])), ''

    def interface_update(self):
        interface_id = self._get(self.req_data, 'interfaceId', 'interface_id', 'id')
        if not interface_id:
            return 0, 'interfaceId 为必传参数'
        result = MockService.update_interface(self.session, interface_id, self.req_data)
        err = self.session.done(close=False)
        return (0, str(err)) if err else (result, '')

    def interface_enable(self):
        interface_id = self._get(self.req_data, 'interfaceId', 'interface_id', 'id')
        if not interface_id:
            return 0, 'interfaceId 为必传参数'
        result = MockService.set_interface_status(self.session, interface_id, 1)
        err = self.session.done(close=False)
        return (0, str(err)) if err else (result, '')

    def interface_disable(self):
        interface_id = self._get(self.req_data, 'interfaceId', 'interface_id', 'id')
        if not interface_id:
            return 0, 'interfaceId 为必传参数'
        result = MockService.set_interface_status(self.session, interface_id, 2)
        err = self.session.done(close=False)
        return (0, str(err)) if err else (result, '')

    def scene_list(self):
        items, total = MockService.list_scenes(self.session, self.req_data)
        data = [MockStatusService.append_scene_text(self.serialize(item, ['is_delete'])) for item in items]
        return {'list': data, 'total': total}

    def scene_update(self):
        scene_id = self._get(self.req_data, 'sceneId', 'scene_id', 'id')
        if not scene_id:
            return 0, 'sceneId 为必传参数'
        result = MockService.update_scene(self.session, scene_id, self.req_data)
        err = self.session.done(close=False)
        return (0, str(err)) if err else (result, '')

    def scene_enable(self):
        scene_id = self._get(self.req_data, 'sceneId', 'scene_id', 'id')
        if not scene_id:
            return 0, 'sceneId 为必传参数'
        result = MockService.set_scene_status(self.session, scene_id, 1)
        err = self.session.done(close=False)
        return (0, str(err)) if err else (result, '')

    def scene_disable(self):
        scene_id = self._get(self.req_data, 'sceneId', 'scene_id', 'id')
        if not scene_id:
            return 0, 'sceneId 为必传参数'
        result = MockService.set_scene_status(self.session, scene_id, 2)
        err = self.session.done(close=False)
        return (0, str(err)) if err else (result, '')

    def log_list(self):
        items, total = MockService.list_logs(self.session, self.req_data)
        return {'list': self.serialize_list(items), 'total': total}

    def parse_issue_list(self):
        items, total = MockService.list_issues(self.session, self.req_data)
        data = [MockStatusService.append_issue_text(self.serialize(item)) for item in items]
        return {'list': data, 'total': total}

    def runtime(self, method, path, query, body, headers):
        response_body, http_status, response_headers, err_msg = MockService.runtime(self.session, method, path, query, body, headers)
        response = make_response(response_body, http_status)
        for key, value in (response_headers or {}).items():
            response.headers[str(key)] = str(value)
        return response, err_msg
