# encoding: UTF-8
from ..model.reportModel import DefectSync, Report
from logger import logger


class ReportDao(object):
    @staticmethod
    def create(session, model_cls, add_info):
        obj = model_cls(**add_info)
        session.add(obj)
        err = session.done(close=False)
        if err:
            logger.warning(f'{model_cls.__name__}新增失败！{err}')
            return 0, f'新增失败！{err}'
        return obj.id, ''

    @staticmethod
    def get_by_id(session, model_cls, obj_id):
        return session.query(model_cls).filter(model_cls.id == int(obj_id)).first()

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page=1, limit=20, order_column=None, asc=False):
        query = session.query(model_cls).filter(*filter_list)
        total = query.count()
        if order_column is not None:
            query = query.order_by(order_column.asc() if asc else order_column.desc())
        rets = query.offset((int(page) - 1) * int(limit)).limit(int(limit)).all()
        return rets, total

    @staticmethod
    def report_model():
        return Report

    @staticmethod
    def defect_model():
        return DefectSync
