# encoding: UTF-8
from ..dao.projectHookDao import ProjectHookDao
from ..model.projectHookModel import ProjectHook


class ProjectHookService(object):
    @staticmethod
    def create(session, model_cls, add_info):
        return ProjectHookDao.create(session, model_cls, add_info)

    @staticmethod
    def update_by_id(session, model_cls, obj_id, update_info, soft_delete=True):
        return ProjectHookDao.update_by_id(session, model_cls, obj_id, update_info, soft_delete)

    @staticmethod
    def get_by_id(session, model_cls, obj_id, soft_delete=True):
        return ProjectHookDao.get_by_id(session, model_cls, obj_id, soft_delete)

    @staticmethod
    def list_by_filters(session, model_cls, filter_list, page_num=1, page_size=20, order_column=None):
        return ProjectHookDao.list_by_filters(session, model_cls, filter_list, int(page_num), int(page_size), order_column)

    @staticmethod
    def delete_by_id(session, model_cls, obj_id):
        return ProjectHookDao.delete_by_id(session, model_cls, obj_id)

    @staticmethod
    def get_hooks_by_project(session, project_id, hook_type=None):
        filters = [
            ProjectHook.project_id == int(project_id),
            ProjectHook.is_delete == 0,
            ProjectHook.enabled == 1
        ]
        if hook_type not in (None, ''):
            filters.append(ProjectHook.hook_type == int(hook_type))
        return ProjectHookDao.list_all_by_filters(session, ProjectHook, filters)