# encoding: UTF-8
from ..dao.caseDao import CaseDao


class CaseService(object):
    """用例域 Service 层，封装用例编号和快照版本等业务能力。"""

    @staticmethod
    def create(session, model_cls, add_info):
        return CaseDao.create(session, model_cls, add_info)

    @staticmethod
    def update_by_id(session, model_cls, obj_id, update_info, soft_delete=True):
        return CaseDao.update_by_id(session, model_cls, obj_id, update_info, soft_delete)

    @staticmethod
    def get_by_id(session, model_cls, obj_id, soft_delete=True):
        return CaseDao.get_by_id(session, model_cls, obj_id, soft_delete)

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page_num=1, page_size=20, order_column=None):
        return CaseDao.list_by_filters(session, model_cls, filter_list, int(page_num), int(page_size), order_column)

    @staticmethod
    def delete_by_id(session, model_cls, obj_id):
        return CaseDao.delete_by_id(session, model_cls, obj_id)

    @staticmethod
    def next_case_key(session, project_id, module_id=None, product_id=None):
        return CaseDao.next_case_key(session, project_id, module_id, product_id)

    @staticmethod
    def next_snapshot_version(session, case_id):
        return CaseDao.next_snapshot_version(session, case_id)

    @staticmethod
    def get_module_name_map(session, module_ids):
        return CaseDao.get_module_name_map(session, module_ids)
