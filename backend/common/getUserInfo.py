from common.getRequest import Request

from const import STRESS_URI


class UserInfo(object):

    @staticmethod
    def get_user_info(access_token, url_prefix=None, info='userId'):
        stress_uri = STRESS_URI
        url = "/back-end/stress/user/info"
        result = Request.go(method="get",
                            url=stress_uri + url if not url_prefix else url_prefix + url,
                            params=None,
                            headers={"accessToken": access_token})
        return None if not result else result.get(info)

    @staticmethod
    def get_user_info_by_user_id(access_token, user_id, info):
        stress_uri = STRESS_URI
        url = "/back-end/stress/user/infoFromId"
        result = Request.go(method="get", url=stress_uri+url, params={'userId': user_id},
                            headers={"accessToken": access_token})
        return None if not result else result.get(info)
