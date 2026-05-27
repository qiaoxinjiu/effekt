# encoding: UTF-8
import json
import uuid
from functools import wraps

import redis
from sqlalchemy.exc import OperationalError
from flask import request, g

from const import REDIS_URL
from common.apiResponse import ApiResponse
from ..service.userService import UserService
from ..service.rbacService import RbacService
from ..model.userModel import User
from common.sqlSession import SqlSession

TOKEN_PREFIX = 'effekt:token:'
TOKEN_CONTEXT_PREFIX = 'effekt:token:ctx:'
REFRESH_TOKEN_PREFIX = 'effekt:refresh:'
TOKEN_EXPIRE_SECONDS = 7200
REFRESH_TOKEN_EXPIRE_SECONDS = 86400 * 7
TOKEN_REFRESH_THRESHOLD_SECONDS = 1800
TOKEN_CONTEXT_EXPIRE_SECONDS = 300
WHITELIST_PATHS = [
    '/it/api/auth/login',
    '/it/api/auth/register',
    '/it/api/auth/refresh',
    '/it/api/automation/execution/case/pull',
    '/it/api/automation/execution/queued',
    '/it/api/automation/execution/start',
    '/it/api/automation/execution/case/result',
    '/it/api/automation/execution/finish',
    '/it/api/automation/execution/abort'
]

_redis_client = redis.from_url(REDIS_URL, decode_responses=True)
_redis_client.ping()


def create_token(user_id):
    token = uuid.uuid4().hex
    key = TOKEN_PREFIX + token
    _redis_client.setex(key, TOKEN_EXPIRE_SECONDS, str(user_id))
    return token, TOKEN_EXPIRE_SECONDS


def create_refresh_token(user_id):
    refresh_token = uuid.uuid4().hex
    key = REFRESH_TOKEN_PREFIX + refresh_token
    _redis_client.setex(key, REFRESH_TOKEN_EXPIRE_SECONDS, str(user_id))
    return refresh_token, REFRESH_TOKEN_EXPIRE_SECONDS


def validate_refresh_token(refresh_token):
    key = REFRESH_TOKEN_PREFIX + refresh_token
    user_id = _redis_client.get(key)
    if user_id:
        return int(user_id)
    return None


def revoke_refresh_token(refresh_token):
    if refresh_token:
        _redis_client.delete(REFRESH_TOKEN_PREFIX + refresh_token)


def revoke_all_refresh_tokens(user_id):
    keys = _redis_client.keys(REFRESH_TOKEN_PREFIX + '*')
    for key in keys:
        stored_user_id = _redis_client.get(key)
        if stored_user_id == str(user_id):
            _redis_client.delete(key)


def get_token_ttl(token):
    return _redis_client.ttl(TOKEN_PREFIX + token)


def refresh_token_if_needed(token):
    ttl = get_token_ttl(token)
    if ttl != -2 and ttl < TOKEN_REFRESH_THRESHOLD_SECONDS:
        _redis_client.expire(TOKEN_PREFIX + token, TOKEN_EXPIRE_SECONDS)
        return TOKEN_EXPIRE_SECONDS
    return ttl


def get_current_user_id(token):
    user_id = _redis_client.get(TOKEN_PREFIX + token)
    return int(user_id) if user_id else 0


def parse_token():
    return request.headers.get('accessToken') or request.headers.get('accesstoken') or request.headers.get('Authorization', '').replace('Bearer ', '')


def get_token_context(token):
    context_str = _redis_client.get(TOKEN_CONTEXT_PREFIX + token)
    return json.loads(context_str) if context_str else None


def cache_token_context(token, user, role_ids, permission_codes):
    _redis_client.setex(TOKEN_CONTEXT_PREFIX + token, TOKEN_CONTEXT_EXPIRE_SECONDS, json.dumps({
        'user': user.to_dict(),
        'role_ids': role_ids,
        'permission_codes': permission_codes
    }, default=str))


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = parse_token()
        if not token:
            return ApiResponse.build_failure(40001, msg='缺少token！')
        user_id = get_current_user_id(token)
        if not user_id:
            return ApiResponse.build_failure(451, msg='token无效或已过期！')
        session = None
        try:
            token_context = get_token_context(token)
            if token_context:
                g.current_user_id = user_id
                g.current_user = token_context.get('user', {})
                g.current_role_ids = token_context.get('role_ids', [])
                g.current_permission_codes = token_context.get('permission_codes', [])
                g.current_token = token
                g.current_token_ttl = refresh_token_if_needed(token)
                return func(*args, **kwargs)
            session = SqlSession()
            user = UserService.get_by_id(session, User, user_id)
            if not user:
                return ApiResponse.build_failure(40011, msg='未查询到对应用户！')
            role_ids = UserService.get_user_role_ids(session, user_id)
            permission_codes = RbacService.get_role_permission_codes(session, role_ids)
            cache_token_context(token, user, role_ids, permission_codes)
            g.current_user_id = user_id
            g.current_user = user
            g.current_role_ids = role_ids
            g.current_permission_codes = permission_codes
            g.current_token = token
            g.current_token_ttl = refresh_token_if_needed(token)
            return func(*args, **kwargs)
        except OperationalError:
            return ApiResponse.build_failure(40008, msg='数据库连接超时，请稍后重试！')
        finally:
            if session:
                session.close()
    return wrapper


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


def permission_required(permission_code):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not getattr(g, 'current_user_id', None):
                return ApiResponse.build_failure(40001, msg='缺少token！')
            current_permission_codes = getattr(g, 'current_permission_codes', [])
            if not has_permission(permission_code, current_permission_codes):
                return ApiResponse.build_failure(40003, msg='无权限访问该接口！')
            return func(*args, **kwargs)
        return wrapper
    return decorator


def should_skip_auth(path):
    return path in WHITELIST_PATHS


def logout_token(token):
    if token:
        _redis_client.delete(TOKEN_PREFIX + token)
        _redis_client.delete(TOKEN_CONTEXT_PREFIX + token)
