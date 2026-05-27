import requests
import json


class FeiShuMessage:

    def __init__(self):
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/180fa48e-1474-448e-a3d5-1a530f6ca689"

    def send_message(self, msg, url=None):
        url = url if url else self.webhook
        res = requests.post(url, headers=self.headers, json=msg, verify=False)
        if res.status_code == 200:
            return True
        else:
            return False

    def is_valid_key_url(self, f_url):
        test_msg_body = {"msg_type": "text", "content": {"text": ""}}
        res = requests.post(f_url, headers=self.headers, json=test_msg_body, verify=False)
        if res.status_code == 200:
            code = json.loads(res.text)['code']
            if code == 19024:
                return True, ''
            else:
                return False, '不是有效的飞书关键字链接，请检查!'
        else:
            return False, '网络异常请稍后重试'


if __name__ == '__main__':
    test = FeiShuMessage()
    msg = req_body = {"msg_type": "text", "content": {"text": ""}}
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/180fa48e-1474-448e-a3d5-1a530f6ca689"
    print(test.is_valid_key_url(url))
