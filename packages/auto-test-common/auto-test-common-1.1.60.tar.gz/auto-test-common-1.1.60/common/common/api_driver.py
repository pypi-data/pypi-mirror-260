import requests
from common.common.constant import Constant
from common.autotest.handle_allure import allure_api_step

class APIDriver(object):

    session = None

    @classmethod
    def get_session(cls):
        if cls.session is None:
            cls.session = requests.Session()
        return cls.session

    @classmethod
    def http_request(cls, url, method, parametric_key=None, header=None, data=None, file=None, cookie=None, _auth=None,
                     desc: str="") -> object:
        """
        :param method: 请求方法
        :param url: 请求url
        :param parametric_key: 入参关键字， params(查询参数类型，明文传输，一般在url?参数名=参数值), data(一般用于form表单类型参数)
        json(一般用于json类型请求参数)
        :param data: 参数数据，默认等于None
        :param file: 文件对象
        :param desc: 自动化测试过程请求描述：打印到Report中
        :param header: 请求头
        :return: 返回res对象
        """
        session = cls.get_session()
        # if url.find(Constant.ATF_PYTHON_URL) > -1 and url.find('login') < 0:
        #     res = session.request(method='post', url=Constant.ATF_PYTHON_URL+"/login", data='{"jwt": "admin2022@"}')
        #     token = res['access_token']
        #     header={'Authorization':f'Bearer {token}'}
        if parametric_key is None:
            res = session.request(method=method, url=url, headers=header, cookies=cookie, auth=_auth)
            allure_api_step(desc, url, method, header, '', '', res)
        elif parametric_key == 'params':
            res = session.request(method=method, url=url, params=data, headers=header, cookies=cookie, auth=_auth)

            allure_api_step(desc, url, method, header, data, '', res)
        elif parametric_key == 'data':
            res = session.request(method=method, url=url, data=data, files=file, headers=header, cookies=cookie,
                                  auth=_auth)
            allure_api_step(desc, url, method, header, data, file, res)
        elif parametric_key == 'json':
            res = session.request(method=method, url=url, json=data, files=file, headers=header, cookies=cookie,
                                  auth=_auth)
            allure_api_step(desc, url, method, header, data, file, res)
        else:
            raise ValueError('可选关键字为params, json, data')
        session.close()
        return res


