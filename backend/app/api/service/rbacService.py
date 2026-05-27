# encoding: UTF-8
from ..dao.rbacDao import RbacDao


def has_permission(permission_code, permission_codes):
    if not permission_code:
        return True
    if not permission_codes:
        return False
    if permission_code in permission_codes:
        return True
    if '*:*' in permission_codes:
        return True
    if ':' in permission_code:
        module_code = permission_code.split(':', 1)[0]
        if f'{module_code}:*' in permission_codes:
            return True
        if '_' in module_code:
            parent_module_code = module_code.split('_', 1)[0]
            if f'{parent_module_code}:*' in permission_codes:
                return True
    return False


class RbacService(object):
    @staticmethod
    def create(session, model_cls, add_info):
        return RbacDao.create(session, model_cls, add_info)

    @staticmethod
    def update_by_id(session, model_cls, obj_id, update_info, soft_delete=True):
        return RbacDao.update_by_id(session, model_cls, obj_id, update_info, soft_delete)

    @staticmethod
    def get_by_id(session, model_cls, obj_id, soft_delete=True):
        return RbacDao.get_by_id(session, model_cls, obj_id, soft_delete)

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page_num=1, page_size=20, order_column=None):
        return RbacDao.list_by_filters(session, model_cls, filter_list, int(page_num), int(page_size), order_column)

    @staticmethod
    def delete_by_id(session, model_cls, obj_id):
        return RbacDao.delete_by_id(session, model_cls, obj_id)

    @staticmethod
    def assign_permissions(session, role_ids, permission_id):
        return RbacDao.assign_permissions_to_roles(session, role_ids, permission_id)

    @staticmethod
    def assign_menus(session, role_id, menu_ids):
        return RbacDao.replace_role_menus(session, role_id, menu_ids)

    @staticmethod
    def get_role_permission_ids(session, role_id):
        return RbacDao.get_role_permission_ids(session, role_id)

    @staticmethod
    def get_role_menu_ids(session, role_id):
        return RbacDao.get_role_menu_ids(session, role_id)

    @staticmethod
    def get_menu_permission_codes(session, menu_ids):
        return RbacDao.get_menu_permission_codes(session, menu_ids)

    @staticmethod
    def get_permission_ids_by_codes(session, permission_codes):
        return RbacDao.get_permission_ids_by_codes(session, permission_codes)

    @staticmethod
    def build_menu_tree(session, filters, role_ids=None, menu_ids=None):
        items = RbacDao.get_menu_tree_items(session, filters)
        visible_ids = set()
        if not role_ids and not menu_ids:
            visible_ids = {item.id for item in items}
        else:
            role_menu_ids = set(menu_ids or [])
            if role_ids:
                for role_id in role_ids:
                    role_menu_ids.update(RbacDao.get_role_menu_ids(session, role_id))
            visible_ids = set(role_menu_ids)
            item_by_id = {item.id: item for item in items}
            for item_id in list(visible_ids):
                if item_id not in item_by_id:
                    continue
                parent_id = item_by_id[item_id].parent_id
                while parent_id and parent_id in item_by_id:
                    if parent_id in visible_ids:
                        break
                    visible_ids.add(parent_id)
                    parent_id = item_by_id[parent_id].parent_id
        item_map = {}
        roots = []
        for item in items:
            if item.id not in visible_ids:
                continue
            item_dict = item.to_dict()
            item_dict['children'] = []
            item_map[item.id] = item_dict
        for item in items:
            if item.id not in item_map:
                continue
            if item.parent_id and item.parent_id in item_map:
                item_map[item.parent_id]['children'].append(item_map[item.id])
            else:
                roots.append(item_map[item.id])
        return roots

    @staticmethod
    def get_role_permission_codes(session, role_ids):
        return RbacDao.get_role_permission_codes(session, role_ids)
