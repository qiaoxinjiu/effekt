# encoding: UTF-8
from ..dao.productDao import ProductDao


class ProductService(object):
    @staticmethod
    def create(session, model_cls, add_info):
        return ProductDao.create(session, model_cls, add_info)

    @staticmethod
    def update_by_id(session, model_cls, obj_id, update_info, soft_delete=True):
        return ProductDao.update_by_id(session, model_cls, obj_id, update_info, soft_delete)

    @staticmethod
    def get_by_id(session, model_cls, obj_id, soft_delete=True):
        return ProductDao.get_by_id(session, model_cls, obj_id, soft_delete)

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page_num=1, page_size=20, order_column=None):
        return ProductDao.list_by_filters(session, model_cls, filter_list, int(page_num), int(page_size), order_column)

    @staticmethod
    def delete_by_id(session, model_cls, obj_id):
        return ProductDao.delete_by_id(session, model_cls, obj_id)
