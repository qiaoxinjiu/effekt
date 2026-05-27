# encoding: UTF-8
from ..dao.updateSqlProjectDao import UpdateSqlProjectDao
from logger import logger


class UpdateSqlProjectService(object):
    def __init__(self):
        pass

    @staticmethod
    def create_sql_project(session, add_info):
        bf_dao = UpdateSqlProjectDao()
        sql_id, err_msg = bf_dao.create_sql_project(session, add_info)
        return sql_id, err_msg

    @staticmethod
    def update_sql_project(session, sql_id, update_info):
        bf_dao = UpdateSqlProjectDao()
        update_res, err_msg = bf_dao.update_sql_project_by_id(session, sql_id, update_info)
        return update_res, err_msg

    @staticmethod
    def get_sql_list_by_filters(session, page_num=1, page_size=20, filter_list=None):
        bf_dao = UpdateSqlProjectDao()
        filter_list = filter_list or []
        bf_obj, count_num = bf_dao.get_sql_by_filters(session, filter_list, int(page_num), int(page_size))
        return bf_obj, count_num

    @staticmethod
    def get_sql_project_by_id(session, sql_id):
        bf_dao = UpdateSqlProjectDao()
        return bf_dao.get_sql_project_by_id(session, sql_id)

    @staticmethod
    def delete_sql_project_by_id(session, sql_id):
        bf_dao = UpdateSqlProjectDao()
        return bf_dao.delete_sql_project_by_id(session, sql_id)
