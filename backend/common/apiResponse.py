# encoding: UTF-8

from flask import make_response
import json
from decimal import Decimal
from const import RES_CODE


class ApiResponse(object):
    def __init__(self):
        self.success = False
        self.code = ''
        self.message = ''
        self.data = {}

    @staticmethod
    def build_success(code=20000, message='', data=None):
        if data is None:
            data = {}
        response = ApiResponse()
        response.success = True
        response.code = code
        response.message = message
        response.data = data
        return response.cors_response(make_response(json.dumps(response, default=obj_2_json)))

    @staticmethod
    def build_failure(code, msg='', data=None):
        response = ApiResponse()
        if data is None:
            data = {}
        if not msg:
            response.message = RES_CODE[code]
        else:
            response.message = msg
        response.success = False
        response.code = code
        response.data = data
        return response.cors_response(make_response(json.dumps(response, default=obj_2_json)))

    @staticmethod
    def cors_response(res):
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return res


def obj_2_json(obj):
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, 'strftime'):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, Decimal):
        return float(obj)
    return {
        'success': obj.success,
        'code': obj.code,
        'message': obj.message,
        'data': obj.data
    }
