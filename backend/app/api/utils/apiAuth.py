# encoding: UTF-8
from logger import logger
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from urllib import parse


class apiAuth(object):

    def __init__(self):
        self.ops_uri = ""
        self.showUsername = ""
        self.username = ""
        self.password = ""
        self.sso_login_url = ""
        self.redirect_url = ""

    def getSsoToken(self):
        session = requests.session()
        post_data = dict()
        post_data['showUsername'] = self.showUsername
        post_data['username'] = self.username
        post_data['password'] = self.password
        session.post(url=self.sso_login_url,data=post_data,allow_redirects=True,verify=False)
        resp = session.get(
            url=self.redirect_url ,
            allow_redirects=False ,
            verify=False)
        resp1 = session.get(
            url=resp.headers['Location'] ,
            allow_redirects=False ,
            verify=False)
        ssoToken = resp1.headers["Set-Cookie"].split("=")[1]
        return ssoToken




if __name__ == '__main__':
    test = apiAuth()
    print(test.getSsoToken())