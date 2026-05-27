# -*- coding: utf-8 -*-
from const import STRESS_URI, QE_DOMAIN

from common.getRequest import Request


class CronRequest(object):
    def __init__(self, token):
        self.stress_api = STRESS_URI
        self.headers = {'accesstoken': token, 'Accept': '*/*', 'content-type': 'application/json;charset=UTF-8'}
        self.qe_domain = QE_DOMAIN

    def create(self, params):
        url = self.stress_api + '/back-end/stress/schedule/save'
        ret = Request.go('post', url, params, self.headers)
        if not ret:
            return
        return ret.get('id')

    def pause(self, jid):
        url = self.stress_api + '/back-end/stress/schedule/pause'
        params = [jid]
        Request.go('post', url, params, self.headers)

    def resume(self, jid):
        url = self.stress_api + '/back-end/stress/schedule/resume'
        params = [jid]
        Request.go('post', url, params, self.headers)

    def remove(self, jid):
        url = self.stress_api + '/back-end/stress/schedule/delete'
        params = [jid]
        Request.go('post', url, params, self.headers)

    def update(self, req_params):
        url = self.stress_api + '/back-end/stress/schedule/update'
        Request.go('post', url, req_params, self.headers)

    def test(self,req_params):
        url = self.stress_api + '/aida/keyword/run'
        print(url)
        b = Request.go('post', url, req_params, self.headers)
        print(b)

    def scrapy(self):
        url = self.stress_api + '/data/detail/scrapy'
        req_params = {"team": "USER", "fileName": "", "username": "", "password": ""}
        b = Request.go('post', url, req_params, self.headers)
        print(b)

    def detail(self):
        url = self.stress_api + '/detail/list'
        req_params = {"team": "USER", "fileName": "", "username": "", "password": ""}
        b = Request.go('get', url, req_params, self.headers)
        print(b)

    def run(self):
        url = "https://172.19.28.91:8088/aida//it/api/create_dialog_by_user"
        # url = self.stress_api + '/create_dialog_by_user'
        req_params = {"user_id":597021,"req_data":"新增用户","issue_id":41}
        b = Request.go('get', url, req_params, self.headers)
        print(b)

    def run_sim(self,req_params):
        url = "http://172.19.28.91:5012/api/aida/keyword/run"
        # url = "http://10.250.201.236:5012/api/aida/keyword/run"
        # url = self.stress_api + '/create_dialog_by_user'
        b = Request.go('post', url, req_params, self.headers)
        print(b)

    def run_xiao(self,req_params):
        url = "https://qe.bg.huohua.cn/back-end/it/api/list_incomplete_special_by_teams"
        # url = "https://qe.bg.huohua.cn/back-end/it/api/get_team_server"
        b = Request.go('post', url, req_params, self.headers)
        print(b)

if __name__ == '__main__':
    test = CronRequest(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoxNDI4MSwidXNlcl9pZCI6MTQyODEsInVzZXJfbmFtZSI6InFpYW94aW5qaXUiLCJzY29wZSI6WyJzZXJ2ZXIiXSwibmFtZSI6Iuiwr-aWsOS5hSIsImV4cCI6MTY5ODc2MzcwMCwiYXV0aG9yaXRpZXMiOlsiUk9MRV9VU0VSIl0sImp0aSI6IjZhMTg1ZWFlLTEyOGQtNDg5Yy05N2Q0LWRlOTM2NzA4ZGZmMSIsImVtYWlsIjoicWlhb3hpbmppdUBzcGFya2VkdS5jb20iLCJjbGllbnRfaWQiOiJlZmZlY3QifQ.L5WeZwyctUl-kto0rejY3PC3J1O5sksRZcA-0yQJQSg")

    # a={'method_name': 'logic_public_add_user_recharge','request_parameter': '{  "phone": "",  "courseId": "",  "classHour": 100}', 'request_id': 1199}
    # a={'method_name': 'kw_tmo_creat_lesson_classroom','request_parameter': '{  "classesId": 1200092722,  "classroom_number": 1}', 'request_id': 1199}
    # a={'method_name': 'logic_cc_create_new_leads', 'request_parameter': '{  "phone": "",  "subject": ""}', 'request_id': 1199}
    # a={'method_name': 'kw_get_class_student','request_parameter': '{  "class_id": 500911139}', 'request_id': 1199}
    import json
    dict_request = {'teacher_id': 'default', 'course_id': 851732, 'start_date': 'default', 'union_flag': 0, 'schedule_info_list': 'default', 'systemUserId': 10697}

    a={'method_name': 'htm_public_classes_create_class','request_parameter': '{"teacher_id": "0", "course_id": 172, "start_date": "default", "union_flag": 0, "weekList": ["default"], "timeList": ["default"], "systemUserId": 586669}', 'request_id': 1199}
    # a={'method_name': 'student_finish_classroom','request_parameter': '{"classroom_code": "CR2310500625595", "student_user_id": 1882444, "systemUserId": 10697}', 'request_id': 1199}
    # a={'method_name': 'kw_create_test_case_robot','request_parameter': '{"systemUserId": "14263", "msg": "我有一个用例，名称为：testcase001，用例步骤如下：\n步骤1：新增一个用户\n步骤2：再新增一个用户\n步骤3：为步骤2的用户购买逻辑思维套餐\n步骤4：新建一个班级\n步骤5：补差升级\n步骤6：将步骤2的用户加入步骤4班级\n步骤7：将步骤1的用户加入步骤4班级\n步骤8：验证补差升级\n请帮忙生成自动化测试用例,请根据以上步骤结合提供的函数和函数返回信息，如果有步骤没有匹配到函数则填写NOKEYWORDS代替，生成一个robotframework的自动化测试用例，每个步骤加上注释"}', 'request_id': 1199}
    # test.test(a)
    b = {'teacher_id': '0', 'course_id': 10101, 'start_date': 'default', 'union_flag': 0, 'weekList': ['default'], 'timeList': ['default'], 'systemUserId': 586669}
    print(json.dumps(b))
    # test.detail()
    # test.scrapy()
    # test.run()
    # test.run_sim(a){"project_plan_id":"2282","team":""}
    sss = {"project_id":2282,"project_plan_id":"2282","team":""}
    test.run_xiao(req_params=sss)