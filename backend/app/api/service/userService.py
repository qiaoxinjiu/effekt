# encoding: UTF-8
from ..dao.userDao import UserDao
from ..dao.rbacDao import RbacDao


class UserService(object):
    @staticmethod
    def create(session, model_cls, add_info):
        return UserDao.create(session, model_cls, add_info)

    @staticmethod
    def update_by_id(session, model_cls, obj_id, update_info, soft_delete=True):
        return UserDao.update_by_id(session, model_cls, obj_id, update_info, soft_delete)

    @staticmethod
    def get_by_id(session, model_cls, obj_id, soft_delete=True):
        return UserDao.get_by_id(session, model_cls, obj_id, soft_delete)

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page_num=1, page_size=20, order_column=None):
        return UserDao.list_by_filters(session, model_cls, filter_list, int(page_num), int(page_size), order_column)

    @staticmethod
    def delete_by_id(session, model_cls, obj_id):
        return UserDao.delete_by_id(session, model_cls, obj_id)

    @staticmethod
    def assign_roles(session, user_id, role_ids):
        return UserDao.replace_user_roles(session, user_id, role_ids)

    @staticmethod
    def get_user_role_ids(session, user_id):
        return UserDao.get_user_role_ids(session, user_id)

    @staticmethod
    def get_user_roles_map(session, user_ids):
        user_role_map = UserDao.get_user_roles(session, user_ids)
        role_ids = list({role_id for role_list in user_role_map.values() for role_id in role_list})
        role_name_map = RbacDao.get_role_names_map(session, role_ids)
        ret = {}
        for user_id, ids in user_role_map.items():
            ret[user_id] = {
                'role_ids': ids,
                'role_names': [role_name_map.get(role_id, '') for role_id in ids]
            }
        return ret

    @staticmethod
    def get_by_username(session, username):
        return UserDao.get_by_username(session, username)

    @staticmethod
    def get_user_info_map(session, user_ids):
        return UserDao.get_user_info_map(session, user_ids)

    @staticmethod
    def update_last_login_time(session, user_id):
        return UserDao.update_last_login_time(session, user_id)
