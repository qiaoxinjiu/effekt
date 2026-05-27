# encoding: UTF-8
from flask import g

from .baseCrudController import BaseCrudController
from ..model.rbacModel import Role, Permission, Menu, RolePermission
from ..service.rbacService import RbacService


class RbacController(BaseCrudController):
    def role_list(self):
        filters = []
        status = self._get(self.req_data, 'status')
        if status not in (None, ''):
            filters.append(Menu.status == int(status))
        return RbacService.build_menu_tree(
            self.session,
            filters,
            role_ids=getattr(g, 'current_role_ids', [])
        )

    def role_page_list(self):
        filters = []
        keyword = self._get(self.req_data, 'keyword')
        status = self._get(self.req_data, 'status')
        if keyword:
            filters.append(Role.name.like('%{}%'.format(keyword)))
        if status not in (None, ''):
            filters.append(Role.status == int(status))
        items, total = RbacService.list_by_filters(self.session, Role, filters,
                                                   self._get(self.req_data, 'pageNo', 'page', default=1),
                                                   self._get(self.req_data, 'pageSize', 'size', default=20),
                                                   Role.created_time)
        return {'list': self.serialize_list(items, ['is_delete']), 'total': total}

    def role_detail(self):
        role_id = self._get(self.req_data, 'roleId', 'id')
        if not role_id:
            return {}, 'roleId 为必传参数'
        item = RbacService.get_by_id(self.session, Role, role_id)
        if not item:
            return {}, '未查询到对应角色！'
        return self.serialize(item, ['is_delete']), ''

    def role_create(self):
        code = self._get(self.req_data, 'code')
        name = self._get(self.req_data, 'name')
        if not code or not name:
            return 0, 'code、name 为必传参数'
        return RbacService.create(self.session, Role, {
            'code': code,
            'name': name,
            'description': self._get(self.req_data, 'description'),
            'status': int(self._get(self.req_data, 'status', default=1)),
            'is_system': int(self._get(self.req_data, 'isSystem', 'is_system', default=0)),
            'created_by': self._get(self.req_data, 'createdBy'),
            'is_delete': 0
        })

    def role_update(self):
        role_id = self._get(self.req_data, 'roleId', 'id')
        if not role_id:
            return 0, 'roleId 为必传参数'
        update_info = {}
        for req_key, column_key in [('code', 'code'), ('name', 'name'), ('description', 'description'),
                                    ('status', 'status'), ('isSystem', 'is_system'), ('is_system', 'is_system')]:
            value = self._get(self.req_data, req_key)
            if value is not None:
                update_info[column_key] = value
        return RbacService.update_by_id(self.session, Role, role_id, update_info)

    def role_delete(self):
        role_id = self._get(self.req_data, 'roleId', 'id')
        if not role_id:
            return 0, 'roleId 为必传参数'
        return RbacService.delete_by_id(self.session, Role, role_id)

    def permission_list(self):
        filters = []
        keyword = self._get(self.req_data, 'keyword')
        module = self._get(self.req_data, 'module')
        status = self._get(self.req_data, 'status')
        if keyword:
            filters.append(Permission.name.like('%{}%'.format(keyword)))
        if module:
            filters.append(Permission.module == module)
        if status not in (None, ''):
            filters.append(Permission.status == int(status))
        items, total = RbacService.list_by_filters(self.session, Permission, filters,
                                                   self._get(self.req_data, 'pageNo', 'page', default=1),
                                                   self._get(self.req_data, 'pageSize', 'size', default=20),
                                                   Permission.created_time)
        role_permission_items = self.session.query(RolePermission).filter(RolePermission.is_delete == 0).all()
        permission_role_map = {}
        for rp in role_permission_items:
            if rp.permission_id not in permission_role_map:
                permission_role_map[rp.permission_id] = []
            permission_role_map[rp.permission_id].append(rp.role_id)
        role_items = self.session.query(Role).filter(Role.is_delete == 0).all()
        role_map = {r.id: {'id': r.id, 'name': r.name} for r in role_items}
        result_list = []
        for item in items:
            item_dict = self.serialize(item, ['is_delete'])
            role_ids = permission_role_map.get(item.id, [])
            item_dict['roles'] = [role_map.get(rid) for rid in role_ids if role_map.get(rid)]
            result_list.append(item_dict)
        return {'list': result_list, 'total': total}

    def permission_detail(self):
        permission_id = self._get(self.req_data, 'permissionId', 'id')
        if not permission_id:
            return {}, 'permissionId 为必传参数'
        item = RbacService.get_by_id(self.session, Permission, permission_id)
        if not item:
            return {}, '未查询到对应权限！'
        return self.serialize(item, ['is_delete']), ''

    def permission_create(self):
        code = self._get(self.req_data, 'code')
        name = self._get(self.req_data, 'name')
        if not code or not name:
            return 0, 'code、name 为必传参数'
        return RbacService.create(self.session, Permission, {
            'code': code,
            'name': name,
            'module': self._get(self.req_data, 'module'),
            'action': self._get(self.req_data, 'action'),
            'description': self._get(self.req_data, 'description'),
            'status': int(self._get(self.req_data, 'status', default=1)),
            'is_delete': 0
        })

    def permission_update(self):
        permission_id = self._get(self.req_data, 'permissionId', 'id')
        if not permission_id:
            return 0, 'permissionId 为必传参数'
        update_info = {}
        for req_key, column_key in [('code', 'code'), ('name', 'name'), ('module', 'module'), ('action', 'action'),
                                    ('description', 'description'), ('status', 'status')]:
            value = self._get(self.req_data, req_key)
            if value is not None:
                update_info[column_key] = value
        return RbacService.update_by_id(self.session, Permission, permission_id, update_info)

    def permission_delete(self):
        permission_id = self._get(self.req_data, 'permissionId', 'id')
        if not permission_id:
            return 0, 'permissionId 为必传参数'
        return RbacService.delete_by_id(self.session, Permission, permission_id)

    def menu_tree(self):
        return RbacService.build_menu_tree(self.session, [])

    def current_menu_list(self):
        filters = []
        status = self._get(self.req_data, 'status')
        if status not in (None, ''):
            filters.append(Menu.status == int(status))
        return RbacService.build_menu_tree(
            self.session,
            filters,
            role_ids=getattr(g, 'current_role_ids', [])
        )

    def role_menu_tree(self):
        role_id = self._get(self.req_data, 'roleId')
        if not role_id:
            return {'tree': [], 'checkedKeys': []}, 'roleId 为必传参数'
        return {
            'tree': RbacService.build_menu_tree(self.session, []),
            'checkedKeys': RbacService.get_role_menu_ids(self.session, role_id)
        }, ''

    def menu_detail(self):
        menu_id = self._get(self.req_data, 'menuId', 'id')
        if not menu_id:
            return {}, 'menuId 为必传参数'
        item = RbacService.get_by_id(self.session, Menu, menu_id)
        if not item:
            return {}, '未查询到对应菜单！'
        return self.serialize(item, ['is_delete']), ''

    def menu_create(self):
        name = self._get(self.req_data, 'name')
        if not name:
            return 0, 'name 为必传参数'
        return RbacService.create(self.session, Menu, {
            'parent_id': int(self._get(self.req_data, 'parentId', 'parent_id', default=0)),
            'name': name,
            'code': self._get(self.req_data, 'code'),
            'type': int(self._get(self.req_data, 'type', default=1)),
            'path': self._get(self.req_data, 'path'),
            'component': self._get(self.req_data, 'component'),
            'icon': self._get(self.req_data, 'icon'),
            'permission_code': self._get(self.req_data, 'permissionCode', 'permission_code'),
            'sort': int(self._get(self.req_data, 'sort', default=0)),
            'visible': int(self._get(self.req_data, 'visible', default=1)),
            'status': int(self._get(self.req_data, 'status', default=1)),
            'is_delete': 0
        })

    def menu_update(self):
        menu_id = self._get(self.req_data, 'menuId', 'id')
        if not menu_id:
            return 0, 'menuId 为必传参数'
        update_info = {}
        field_pairs = [
            (('parentId', 'parent_id'), 'parent_id'),
            (('name',), 'name'),
            (('code',), 'code'),
            (('type',), 'type'),
            (('permissionCode', 'permission_code'), 'permission_code'),
            (('sort',), 'sort'),
            (('visible',), 'visible'),
            (('status',), 'status')
        ]
        for req_keys, column_key in field_pairs:
            value = self._get(self.req_data, *req_keys)
            if value is not None:
                update_info[column_key] = value
        
        for key in ['path', 'component', 'icon']:
            if key in self.req_data:
                update_info[key] = self.req_data[key]
        
        return RbacService.update_by_id(self.session, Menu, menu_id, update_info)

    def menu_delete(self):
        menu_id = self._get(self.req_data, 'menuId', 'id')
        if not menu_id:
            return 0, 'menuId 为必传参数'
        
        menu = RbacService.get_by_id(self.session, Menu, menu_id)
        if menu and menu.permission_code:
            permission = self.session.query(Permission).filter(
                Permission.code == menu.permission_code,
                Permission.is_delete == 0
            ).first()
            if permission:
                self.session.query(RolePermission).filter(
                    RolePermission.permission_id == permission.id,
                    RolePermission.is_delete == 0
                ).update({'is_delete': 1})
        
        return RbacService.delete_by_id(self.session, Menu, menu_id)

    def role_permission_list(self):
        role_id = self._get(self.req_data, 'roleId')
        if not role_id:
            return {'permissionIds': []}
        return {'permissionIds': RbacService.get_role_permission_ids(self.session, role_id)}

    def role_permission_assign(self):
        role_ids = self._get(self.req_data, 'roleIds', default=[])
        permission_id = self._get(self.req_data, 'permissionId')
        if not role_ids:
            return 0, 'roleIds 为必传参数'
        if not permission_id:
            return 0, 'permissionId 为必传参数'
        return RbacService.assign_permissions(self.session, role_ids, permission_id)

    def role_menu_list(self):
        role_id = self._get(self.req_data, 'roleId')
        if not role_id:
            return {'menuIds': []}
        return {'menuIds': RbacService.get_role_menu_ids(self.session, role_id)}

    def role_menu_assign(self):
        role_id = self._get(self.req_data, 'roleId')
        menu_ids = self._get(self.req_data, 'menuIds', default=[])
        if not role_id:
            return 0, 'roleId 为必传参数'
        
        if isinstance(menu_ids, str):
            import json
            menu_ids = json.loads(menu_ids)
        if not isinstance(menu_ids, list):
            menu_ids = []
        
        menu_permission_codes = RbacService.get_menu_permission_codes(self.session, menu_ids)
        
        permission_ids = RbacService.get_permission_ids_by_codes(self.session, menu_permission_codes)
        
        existing_permission_ids = RbacService.get_role_permission_ids(self.session, role_id)
        
        deleted_permission_ids = [pid for pid in existing_permission_ids if pid not in permission_ids]
        if deleted_permission_ids:
            self.session.query(RolePermission).filter(
                RolePermission.role_id == int(role_id),
                RolePermission.permission_id.in_(deleted_permission_ids),
                RolePermission.is_delete == 0
            ).update({'is_delete': 1})
        
        new_permission_ids = [pid for pid in permission_ids if pid not in existing_permission_ids]
        if new_permission_ids:
            existing_deleted = self.session.query(RolePermission).filter(
                RolePermission.role_id == int(role_id),
                RolePermission.permission_id.in_(new_permission_ids),
                RolePermission.is_delete == 1
            ).all()
            existing_deleted_map = {rp.permission_id: rp for rp in existing_deleted}
            
            for permission_id in new_permission_ids:
                if permission_id in existing_deleted_map:
                    existing_deleted_map[permission_id].is_delete = 0
                else:
                    self.session.add(RolePermission(
                        role_id=int(role_id),
                        permission_id=permission_id,
                        is_delete=0
                    ))
        
        return RbacService.assign_menus(self.session, role_id, menu_ids)
