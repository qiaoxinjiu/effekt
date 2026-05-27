# encoding: UTF-8
from datetime import datetime

from common.dataBuilderExecutor import DataBuilderExecutor
from ..dao.dataBuilderDao import DataBuilderDao
from ..model.dataBuilderModel import DataBuilder, DataTask


class DataBuilderService(object):
    @staticmethod
    def create(session, model_cls, add_info):
        return DataBuilderDao.create(session, model_cls, add_info)

    @staticmethod
    def update_by_id(session, model_cls, obj_id, update_info, soft_delete=True):
        return DataBuilderDao.update_by_id(session, model_cls, obj_id, update_info, soft_delete)

    @staticmethod
    def get_by_id(session, model_cls, obj_id, soft_delete=True):
        return DataBuilderDao.get_by_id(session, model_cls, obj_id, soft_delete)

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page_num=1, page_size=20, order_column=None):
        return DataBuilderDao.list_by_filters(session, model_cls, filter_list, int(page_num), int(page_size), order_column)

    @staticmethod
    def delete_by_id(session, model_cls, obj_id):
        return DataBuilderDao.delete_by_id(session, model_cls, obj_id)

    @staticmethod
    def execute_builder(session, builder_id, params=None, created_by=None):
        builder = DataBuilderDao.get_by_id(session, DataBuilder, builder_id)
        if not builder:
            return {}, '未查询到对应造数器！'
        params = params or {}
        task_info = {
            'builder_id': builder.id,
            'project_id': builder.project_id,
            'params': params,
            'status': 1,
            'created_by': created_by
        }
        # 先写入执行中任务，保证失败时也能追踪任务记录。
        task_id, err_msg = DataBuilderDao.create(session, DataTask, task_info)
        if err_msg:
            return {}, err_msg
        try:
            # 当前 MVP 只做同步模板渲染执行，后续可在 executor 内扩展 http/db step。
            executor = DataBuilderExecutor(builder.definition or {}, {})
            result_data = executor.execute(params)
            DataBuilderDao.update_by_id(session, DataTask, task_id, {
                'status': 2,
                'result_data': result_data,
                'completed_time': datetime.now()
            }, soft_delete=False)
            return {'taskId': task_id, 'data': result_data}, ''
        except Exception as e:
            DataBuilderDao.update_by_id(session, DataTask, task_id, {
                'status': 3,
                'error_message': str(e),
                'completed_time': datetime.now()
            }, soft_delete=False)
            return {}, f'执行造数失败！{e}'
