# encoding: UTF-8
from ..dao.projectDao import ProjectDao


class ProjectService(object):
    """项目域 Service 层，保持业务入口与 DAO 解耦。"""

    @staticmethod
    def create(session, model_cls, add_info):
        return ProjectDao.create(session, model_cls, add_info)

    @staticmethod
    def update_by_id(session, model_cls, obj_id, update_info, soft_delete=True):
        return ProjectDao.update_by_id(session, model_cls, obj_id, update_info, soft_delete)

    @staticmethod
    def get_by_id(session, model_cls, obj_id, soft_delete=True):
        return ProjectDao.get_by_id(session, model_cls, obj_id, soft_delete)

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page_num=1, page_size=20, order_column=None):
        return ProjectDao.list_by_filters(session, model_cls, filter_list, int(page_num), int(page_size), order_column)

    @staticmethod
    def delete_by_id(session, model_cls, obj_id):
        return ProjectDao.delete_by_id(session, model_cls, obj_id)

    @staticmethod
    def get_product_map(session, product_ids):
        return ProjectDao.get_product_map(session, product_ids)

    @staticmethod
    def get_project_name_map(session, project_ids):
        return ProjectDao.get_project_name_map(session, project_ids)
