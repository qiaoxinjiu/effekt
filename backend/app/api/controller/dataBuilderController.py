# encoding: UTF-8
from .baseCrudController import BaseCrudController
from ..model.dataBuilderModel import DataBuilder, DataTask
from ..service.dataBuilderService import DataBuilderService


class DataBuilderController(BaseCrudController):
    """造数器与造数任务相关接口控制器。"""

    def builder_list(self):
        """分页查询造数器列表，可按项目过滤。"""
        filters = []
        project_id = self._get(self.req_data, 'projectId')
        if project_id:
            filters.append(DataBuilder.project_id == int(project_id))
        items, total = DataBuilderService.list_by_filters(self.session, DataBuilder, filters,
                                                          self._get(self.req_data, 'pageNo', default=1),
                                                          self._get(self.req_data, 'pageSize', default=20),
                                                          DataBuilder.created_time)
        return {'list': self.serialize_list(items, ['is_delete']), 'total': total}

    def builder_detail(self):
        """查询造数器详情。"""
        builder_id = self._get(self.req_data, 'builderId', 'id')
        if not builder_id:
            return {}, 'builderId 为必传参数'
        item = DataBuilderService.get_by_id(self.session, DataBuilder, builder_id)
        if not item:
            return {}, '未查询到对应造数器！'
        return self.serialize(item, ['is_delete']), ''

    def builder_create(self):
        """创建造数器，definition 保存流程编排或模板定义。"""
        project_id = self._get(self.req_data, 'projectId')
        name = self._get(self.req_data, 'name')
        definition = self._get(self.req_data, 'definition')
        if not project_id or not name or definition is None:
            return 0, 'projectId、name、definition 为必传参数'
        add_info = {'project_id': project_id, 'name': name, 'description': self._get(self.req_data, 'description'),
                    'builder_type': int(self._get(self.req_data, 'builderType', default=1)), 'definition': definition,
                    'input_schema': self._get(self.req_data, 'inputSchema'),
                    'output_example': self._get(self.req_data, 'outputExample'),
                    'created_by': self._get(self.req_data, 'createdBy'), 'is_delete': 0}
        return DataBuilderService.create(self.session, DataBuilder, add_info)

    def builder_update(self):
        builder_id = self._get(self.req_data, 'builderId', 'id')
        if not builder_id:
            return 0, 'builderId 为必传参数'
        update_info = {}
        for req_key, column_key in [('name', 'name'), ('description', 'description'), ('builderType', 'builder_type'),
                                    ('definition', 'definition'), ('inputSchema', 'input_schema'),
                                    ('outputExample', 'output_example')]:
            value = self._get(self.req_data, req_key)
            if value is not None:
                update_info[column_key] = value
        return DataBuilderService.update_by_id(self.session, DataBuilder, builder_id, update_info)

    def builder_delete(self):
        builder_id = self._get(self.req_data, 'builderId', 'id')
        if not builder_id:
            return 0, 'builderId 为必传参数'
        return DataBuilderService.delete_by_id(self.session, DataBuilder, builder_id)

    def builder_execute(self):
        builder_id = self._get(self.req_data, 'builderId')
        if not builder_id:
            return {}, 'builderId 为必传参数'
        return DataBuilderService.execute_builder(self.session, builder_id,
                                                  self._get(self.req_data, 'params', default={}),
                                                  self._get(self.req_data, 'createdBy'))

    def task_status(self):
        task_id = self._get(self.req_data, 'taskId')
        if not task_id:
            return {}, 'taskId 为必传参数'
        item = DataBuilderService.get_by_id(self.session, DataTask, task_id, soft_delete=False)
        if not item:
            return {}, '未查询到对应任务！'
        return self.serialize(item), ''
