# -*- coding: utf-8 -*-
import requests
import json
from requests.exceptions import ConnectionError

from logger import logger


class Request(object):

    @classmethod
    def go(cls, method, url, params, headers=None, noFormat=False):
        # logger.info(f'发送{method}请求到: {url}, 参数： {params}')
        try:
            if method == 'get':
                response = requests.get(url=url, params=params, headers=headers, timeout=200)
            elif method == 'post':
                response = requests.post(url=url, data=json.dumps(params), headers=headers, timeout=200)
            else:
                logger.error(f'暂不支持{method}方法')
                return
        except ConnectionRefusedError:
            logger.error(f'服务请求失败：{url}')
            return
        except ConnectionError:
            logger.error(f'服务无法链接： {url}')
            return
        if response.status_code != 200:
            logger.error(f'返回码不等于200，请检查服务！{response.status_code}, {response.text}')
        else:
            resp_json = response.json()
            # logger.info(f'返回内容：{resp_json}')
            # noFormat: 不需要对返回内容进行校验，直接返回整个response
            if noFormat:
                return resp_json
            # 对response做校验，返回体为qe平台的通用格式
            if resp_json.get('success') or resp_json.get('code') == 20000:
                return resp_json.get('data')
            else:
                logger.error(resp_json)
                return
