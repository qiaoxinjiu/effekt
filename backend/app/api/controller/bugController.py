# encoding: UTF-8
import os
import uuid
from datetime import datetime
from flask import current_app

from .baseCrudController import BaseCrudController
from ..model.bugModel import Bug, BugComment
from ..model.productModel import Product
from ..model.projectModel import Project
from ..model.userModel import User
from ..model.caseModel import Module
from ..service.bugService import BugService
from ..service.userService import UserService


class BugUploadController(BaseCrudController):
    UPLOAD_FOLDER = 'attachment/bug_picture'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def bug_upload(self):
        if 'file' not in self.req_data.files:
            return '', '未找到上传文件'

        file = self.req_data.files['file']
        if file.filename == '':
            return '', '文件名不能为空'

        if not self.allowed_file(file.filename):
            return '', '不支持的文件格式，仅支持：png, jpg, jpeg, gif, bmp'

        try:
            os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            ext = file.filename.rsplit('.', 1)[1].lower()
            new_filename = f'bug-{timestamp}-{uuid.uuid4().hex[:8]}.{ext}'
            file_path = os.path.join(self.UPLOAD_FOLDER, new_filename)
            file.save(file_path)

            file_url = f'/uploads/{new_filename}'
            return file_url, ''
        except Exception as e:
            return '', f'文件上传失败：{str(e)}'


class BugController(BaseCrudController):
    def bug_list(self):
        filters = []
        product_id = self._get(self.req_data, 'productId', 'product_id')
        project_id = self._get(self.req_data, 'projectId', 'project_id')
        module_id = self._get(self.req_data, 'moduleId', 'module_id')
        bug_type = self._get(self.req_data, 'bugType', 'bug_type')
        severity = self._get(self.req_data, 'severity')
        priority = self._get(self.req_data, 'priority')
        status = self._get(self.req_data, 'status')
        assignee_id = self._get(self.req_data, 'assigneeId', 'assignee_id')
        reporter_id = self._get(self.req_data, 'reporterId', 'reporter_id')
        resolved_by = self._get(self.req_data, 'resolvedBy', 'resolved_by')
        reproduce_rate = self._get(self.req_data, 'reproduceRate', 'reproduce_rate')
        keyword = self._get(self.req_data, 'keyword')

        if product_id:
            filters.append(Bug.product_id == int(product_id))
        if project_id:
            filters.append(Bug.project_id == int(project_id))
        if module_id:
            filters.append(Bug.module_id == int(module_id))
        if bug_type not in (None, ''):
            filters.append(Bug.bug_type == int(bug_type))
        if severity not in (None, ''):
            filters.append(Bug.severity == int(severity))
        if priority not in (None, ''):
            filters.append(Bug.priority == int(priority))
        if status not in (None, ''):
            filters.append(Bug.status == int(status))
        if assignee_id:
            filters.append(Bug.assignee_id == int(assignee_id))
        if reporter_id:
            filters.append(Bug.reporter_id == int(reporter_id))
        if resolved_by:
            filters.append(Bug.resolved_by == int(resolved_by))
        if reproduce_rate not in (None, ''):
            filters.append(Bug.reproduce_rate == int(reproduce_rate))
        if keyword:
            filters.append(Bug.title.like(f'%{keyword}%') | Bug.description.like(f'%{keyword}%'))

        items, total = BugService.list_by_filters(
            self.session, Bug, filters,
            self._get(self.req_data, 'pageNo', 'page', default=1),
            self._get(self.req_data, 'pageSize', 'size', default=20),
            Bug.created_time
        )
        
        user_ids = []
        for item in items:
            if item.assignee_id:
                user_ids.append(item.assignee_id)
            if item.reporter_id:
                user_ids.append(item.reporter_id)
            if item.resolved_by:
                user_ids.append(item.resolved_by)
        
        user_info_map = UserService.get_user_info_map(self.session, user_ids) if user_ids else {}
        
        result_list = []
        for item in items:
            bug_dict = item.to_dict()
            if item.assignee_id and item.assignee_id in user_info_map:
                bug_dict['assignee_name'] = user_info_map[item.assignee_id].get('real_name', '')
            else:
                bug_dict['assignee_name'] = ''
            if item.reporter_id and item.reporter_id in user_info_map:
                bug_dict['reporter_name'] = user_info_map[item.reporter_id].get('real_name', '')
            else:
                bug_dict['reporter_name'] = ''
            if item.resolved_by and item.resolved_by in user_info_map:
                bug_dict['resolved_by_name'] = user_info_map[item.resolved_by].get('real_name', '')
            else:
                bug_dict['resolved_by_name'] = ''
            result_list.append(bug_dict)
        
        return {'list': result_list, 'total': total}

    def bug_detail(self):
        bug_id = self._get(self.req_data, 'bugId', 'id')
        if not bug_id:
            return {}, 'bugId 为必传参数'
        item = BugService.get_by_id(self.session, Bug, bug_id)
        if not item:
            return {}, '未查询到对应 Bug！'
        ret = self.serialize(item, ['is_delete'])
        
        if item.product_id:
            product = self.session.query(Product).filter(Product.id == item.product_id, Product.is_delete == 0).first()
            ret['product_name'] = product.name if product else ''
        
        if item.project_id:
            project = self.session.query(Project).filter(Project.id == item.project_id, Project.is_delete == 0).first()
            ret['project_name'] = project.name if project else ''
        
        if item.reporter_id:
            reporter = self.session.query(User).filter(User.id == item.reporter_id, User.is_delete == 0).first()
            ret['reporter_name'] = reporter.real_name if reporter else ''
        
        if item.assignee_id:
            assignee = self.session.query(User).filter(User.id == item.assignee_id, User.is_delete == 0).first()
            ret['assignee_name'] = assignee.real_name if assignee else ''
        
        if item.module_id:
            module = self.session.query(Module).filter(Module.id == item.module_id, Module.is_delete == 0).first()
            ret['module_name'] = module.name if module else ''
        
        if item.resolved_by:
            resolved_by_user = self.session.query(User).filter(User.id == item.resolved_by, User.is_delete == 0).first()
            ret['resolved_by_name'] = resolved_by_user.real_name if resolved_by_user else ''
        
        comments = BugService.get_comments(self.session, bug_id)
        comment_user_ids = [c.user_id for c in comments if c.user_id]
        user_info_map = UserService.get_user_info_map(self.session, comment_user_ids) if comment_user_ids else {}
        serialized_comments = []
        for comment in comments:
            comment_dict = comment.to_dict()
            if comment.user_id and comment.user_id in user_info_map:
                comment_dict['user_name'] = user_info_map[comment.user_id].get('real_name', '')
            else:
                comment_dict['user_name'] = ''
            serialized_comments.append(comment_dict)
        ret['comments'] = serialized_comments
        
        history_items = BugService.get_history(self.session, bug_id)
        user_ids = set()
        for h in history_items:
            if h.operator_id:
                user_ids.add(h.operator_id)
            if h.field_name in ('assignee_id', 'reporter_id', 'user_id', 'resolved_by'):
                if h.old_value:
                    try:
                        user_ids.add(int(h.old_value))
                    except (ValueError, TypeError):
                        pass
                if h.new_value:
                    try:
                        user_ids.add(int(h.new_value))
                    except (ValueError, TypeError):
                        pass
        
        user_info_map = UserService.get_user_info_map(self.session, list(user_ids)) if user_ids else {}
        
        serialized_history = []
        for h in history_items:
            h_dict = h.to_dict()
            if h.operator_id:
                h_dict['operator_id'] = user_info_map.get(h.operator_id, {}).get('real_name', h.operator_id)
            if h.field_name in ('assignee_id', 'reporter_id', 'user_id', 'resolved_by'):
                if h.old_value:
                    try:
                        old_uid = int(h.old_value)
                        h_dict['old_value'] = user_info_map.get(old_uid, {}).get('real_name', h.old_value)
                    except (ValueError, TypeError):
                        pass
                if h.new_value:
                    try:
                        new_uid = int(h.new_value)
                        h_dict['new_value'] = user_info_map.get(new_uid, {}).get('real_name', h.new_value)
                    except (ValueError, TypeError):
                        pass
            serialized_history.append(h_dict)
        
        ret['history'] = serialized_history
        return ret, ''

    def bug_create(self):
        title = self._get(self.req_data, 'title')
        product_id = self._get(self.req_data, 'productId', 'product_id')
        project_id = self._get(self.req_data, 'projectId', 'project_id')
        if not title or not product_id or not project_id:
            return 0, 'title、productId、projectId 为必传参数'

        bug_key = BugService.generate_bug_key(self.session)
        add_info = {
            'bug_key': bug_key,
            'title': title,
            'description': self._get(self.req_data, 'description'),
            'bug_type': int(self._get(self.req_data, 'bugType', 'bug_type', default=1)),
            'severity': int(self._get(self.req_data, 'severity', default=2)),
            'priority': int(self._get(self.req_data, 'priority', default=2)),
            'status': 0,
            'reporter_id': self._get(self.req_data, 'reporterId', 'reporter_id'),
            'assignee_id': self._get(self.req_data, 'assigneeId', 'assignee_id'),
            'product_id': product_id,
            'project_id': project_id,
            'module_id': self._get(self.req_data, 'moduleId', 'module_id'),
            'case_id': self._get(self.req_data, 'caseId', 'case_id'),
            'plan_id': self._get(self.req_data, 'planId', 'plan_id'),
            'environment': self._get(self.req_data, 'environment'),
            'steps': self._get(self.req_data, 'steps'),
            'solution': self._get(self.req_data, 'solution'),
            'resolve_version': self._get(self.req_data, 'resolveVersion', 'resolve_version'),
            'resolved_by': self._get(self.req_data, 'resolvedBy', 'resolved_by'),
            'reproduce_rate': self._get(self.req_data, 'reproduceRate', 'reproduce_rate'),
            'is_delete': 0
        }
        return BugService.create(self.session, Bug, add_info)

    def bug_update(self):
        bug_id = self._get(self.req_data, 'bugId', 'id')
        if not bug_id:
            return 0, 'bugId 为必传参数'

        update_info = {}
        field_mapping = [
            (('title',), 'title'),
            (('description',), 'description'),
            (('bugType', 'bug_type'), 'bug_type'),
            (('severity',), 'severity'),
            (('priority',), 'priority'),
            (('status',), 'status'),
            (('assigneeId', 'assignee_id'), 'assignee_id'),
            (('reporterId', 'reporter_id'), 'reporter_id'),
            (('moduleId', 'module_id'), 'module_id'),
            (('caseId', 'case_id'), 'case_id'),
            (('planId', 'plan_id'), 'plan_id'),
            (('environment',), 'environment'),
            (('steps',), 'steps'),
            (('solution',), 'solution'),
            (('resolveVersion', 'resolve_version'), 'resolve_version'),
            (('resolvedBy', 'resolved_by'), 'resolved_by'),
            (('reproduceRate', 'reproduce_rate'), 'reproduce_rate')
        ]

        for req_keys, column_key in field_mapping:
            value = self._get(self.req_data, *req_keys)
            if value is not None:
                update_info[column_key] = value

        result = BugService.update_by_id(self.session, Bug, bug_id, update_info)
        
        comment = self._get(self.req_data, 'comment')
        user_id = self._get(self.req_data, 'user_id', 'userId')
        if comment and user_id:
            BugService.add_comment(self.session, bug_id, comment, user_id)
        
        return result

    def bug_delete(self):
        bug_id = self._get(self.req_data, 'bugId', 'id')
        if not bug_id:
            return 0, 'bugId 为必传参数'
        return BugService.delete_by_id(self.session, Bug, bug_id)

    def bug_history_add(self):
        bug_id = self._get(self.req_data, 'bugId', 'id')
        field_name = self._get(self.req_data, 'fieldName', 'field_name')
        old_value = self._get(self.req_data, 'oldValue', 'old_value')
        new_value = self._get(self.req_data, 'newValue', 'new_value')
        operator_id = self._get(self.req_data, 'operatorId', 'operator_id', 'user_id', 'userId')
        
        if not bug_id:
            return 0, 'bugId 为必传参数'
        if not field_name:
            return 0, 'fieldName 为必传参数'
        if not operator_id:
            return 0, 'operatorId 为必传参数'
        
        success = BugService.add_history(self.session, bug_id, field_name, old_value, new_value, operator_id)
        return 1 if success else 0, '' if success else '添加历史记录失败'

    def bug_comment_add(self):
        user_id = self._get(self.req_data, 'user_id', 'reporter_id', 'reporterId')
        bug_id = self._get(self.req_data, 'bugId')
        content = self._get(self.req_data, 'content')
        if not bug_id:
            return 0, 'bugId 为必传参数'
        if not content:
            return 0, 'content 为必传参数'
        return BugService.add_comment(self.session, bug_id, content, user_id)

    def bug_stats(self):
        product_id = self._get(self.req_data, 'productId', 'product_id')
        project_id = self._get(self.req_data, 'projectId', 'project_id')
        return BugService.get_stats(self.session, product_id, project_id)
