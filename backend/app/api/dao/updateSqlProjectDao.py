# encoding: UTF-8
from ..model.updateSqlProjectModel import UpdateSqlProject
from logger import logger


class UpdateSqlProjectDao(object):

    @staticmethod
    def get_sql_project_by_id(session, sql_id):
        return session.query(UpdateSqlProject).filter(
            UpdateSqlProject.id == int(sql_id), UpdateSqlProject.is_delete == 0
        ).first()

    @staticmethod
    def delete_sql_project_by_id(session, sql_id):
        delete_res = session.query(UpdateSqlProject).filter(
            UpdateSqlProject.id == int(sql_id), UpdateSqlProject.is_delete == 0
        ).update({'is_delete': 1})
        err = session.done(close=False)
        if err:
            logger.error('delete update_sql_project db失败！sql_id: {}, err: {}'.format(sql_id, err))
            return 0, f'删除记录失败！{err}'
        if not delete_res:
            return 0, '未查询到对应记录！'
        return int(sql_id), ''

    @staticmethod
    def create_sql_project(session, add_info):
        if not isinstance(add_info, dict):
            logger.error('create_sql_project不支持其他类型。')
            return 0, '入参类型错误！'
        sql_project_obj = UpdateSqlProject(**add_info)
        session.add(sql_project_obj)
        err = session.done(close=False)
        create_id = sql_project_obj.id
        if err:
            logger.warning(f'create_sql_project新增记录失败！{err}')
            return 0, f'新增记录失败！{err}'
        if not create_id:
            logger.warning('获取update_sql_project记录id失败！')
            return 0, f'{add_info}获取update_sql_project记录id失败！'
        return create_id, ''

    @staticmethod
    def get_sql_by_filters(session, filter_list, page=1, limit=20):
        query = session.query(UpdateSqlProject).filter(*filter_list).filter(UpdateSqlProject.is_delete == 0)
        total = query.count()
        rets = query.order_by(UpdateSqlProject.created_time.desc()) \
            .offset((int(page) - 1) * int(limit)) \
            .limit(limit) \
            .all()
        return rets, total

    @staticmethod
    def update_sql_project_by_id(session, sql_id, update_info):
        update_res = session.query(UpdateSqlProject).filter(
            UpdateSqlProject.id == int(sql_id), UpdateSqlProject.is_delete == 0
        ).update(update_info)
        err = session.done(close=False)
        if err:
            logger.error('update update_sql_project db失败！sql_id: {}, update_info:{}, err: {}'.format(sql_id, update_info, err))
            return 0, f'更新记录失败！{err}'
        if not update_res:
            return 0, '未查询到对应记录！'
        return int(sql_id), ''
