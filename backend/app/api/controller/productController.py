# encoding: UTF-8
import random

from .baseCrudController import BaseCrudController
from ..model.productModel import Product
from ..service.productService import ProductService


class ProductController(BaseCrudController):
    """产品相关接口控制器。"""

    def product_list(self):
        filters = []
        keyword = self._get(self.req_data, 'keyword')
        status = self._get(self.req_data, 'status')
        if keyword:
            filters.append(Product.name.like('%{}%'.format(keyword)))
        if status not in (None, ''):
            filters.append(Product.status == int(status))
        items, total = ProductService.list_by_filters(self.session, Product, filters,
                                                      self._get(self.req_data, 'pageNo', 'page', default=1),
                                                      self._get(self.req_data, 'pageSize', 'size', default=20),
                                                      Product.created_time)
        return {'list': self.serialize_list(items, ['is_delete']), 'total': total}

    def product_detail(self):
        product_id = self._get(self.req_data, 'productId', 'id')
        if not product_id:
            return {}, 'productId 为必传参数'
        item = ProductService.get_by_id(self.session, Product, product_id)
        if not item:
            return {}, '未查询到对应产品！'
        return self.serialize(item, ['is_delete']), ''

    def product_create(self):
        name = self._get(self.req_data, 'name')
        if not name:
            return 0, 'name 为必传参数'
        add_info = {
            'name': name,
            'code': str(random.randint(100000, 999999)),
            'description': self._get(self.req_data, 'description'),
            'status': int(self._get(self.req_data, 'status', default=1)),
            'is_delete': 0
        }
        return ProductService.create(self.session, Product, add_info)

    def product_update(self):
        product_id = self._get(self.req_data, 'productId', 'id')
        if not product_id:
            return 0, 'productId 为必传参数'
        update_info = {}
        for req_key, column_key in [('name', 'name'), ('code', 'code'), ('description', 'description'),
                                    ('status', 'status')]:
            value = self._get(self.req_data, req_key)
            if value is not None:
                update_info[column_key] = value
        return ProductService.update_by_id(self.session, Product, product_id, update_info)

    def product_delete(self):
        product_id = self._get(self.req_data, 'productId', 'id')
        if not product_id:
            return 0, 'productId 为必传参数'
        return ProductService.delete_by_id(self.session, Product, product_id)
