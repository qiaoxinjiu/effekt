# encoding: UTF-8
from ..dao.bugDao import BugDao
from ..model.bugModel import BugComment


class BugService(object):
    """Bug 管理 Service 层"""

    @staticmethod
    def create(session, model_cls, add_info):
        return BugDao.create(session, model_cls, add_info)

    @staticmethod
    def update_by_id(session, model_cls, obj_id, update_info, soft_delete=True):
        return BugDao.update_by_id(session, model_cls, obj_id, update_info, soft_delete)

    @staticmethod
    def get_by_id(session, model_cls, obj_id, soft_delete=True):
        return BugDao.get_by_id(session, model_cls, obj_id, soft_delete)

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page_num=1, page_size=20, order_column=None, asc=False):
        return BugDao.list_by_filters(session, model_cls, filter_list, int(page_num), int(page_size), order_column, asc)

    @staticmethod
    def delete_by_id(session, model_cls, obj_id):
        return BugDao.delete_by_id(session, model_cls, obj_id)

    @staticmethod
    def get_comments(session, bug_id):
        return BugDao.get_comments(session, bug_id)

    @staticmethod
    def get_history(session, bug_id):
        return BugDao.get_history(session, bug_id)

    @staticmethod
    def add_comment(session, bug_id, content, user_id):
        return BugDao.create(session, BugComment, {
            'bug_id': bug_id,
            'content': content,
            'user_id': user_id
        })

    @staticmethod
    def generate_bug_key(session):
        return BugDao.generate_bug_key(session)

    @staticmethod
    def get_stats(session, product_id=None, project_id=None):
        return BugDao.get_stats(session, product_id, project_id)

    @staticmethod
    def add_history(session, bug_id, field_name, old_value, new_value, operator_id):
        return BugDao.add_history(session, bug_id, field_name, old_value, new_value, operator_id)