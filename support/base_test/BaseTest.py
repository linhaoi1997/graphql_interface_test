import jsonpath
from support.tools.log import logger, pformat
from ..caps.read_yaml import config
from ..tools import go_allure
from support.tools.find_gralhql_schema import graphql_query
from .AssertMethod import AssertMethod
from sgqlc.endpoint.http import HTTPEndpoint
import ssl
import pytest
import os


class BaseTestCase(AssertMethod):
    # 不能使用__init__方法，pytest不识别，所以把基本配置当作类变量
    all_param = {
        "list_len": 3,
        "num": 1,
        "is_random": True,
        "no_none": True,
    }
    base_url = config.get_web_information('url')
    headers = {"Content-Type": "application/json"}
    graphql_client = HTTPEndpoint(base_url, headers)

    # 发送请求
    def send_request(self, query, variables):
        logger.debug("variables : " + pformat(variables))
        result = self.graphql_client(query, variables)
        logger.debug("get result : " + pformat(result))
        return result, variables

    # 更新url
    def update_url(self, query_name):
        self.base_url = self.base_url + "?" + query_name
        self.graphql_client = HTTPEndpoint(self.base_url, self.headers)

    @classmethod
    def login(cls, account, password):
        token = login(account, password)
        cls.update_token(token)

    @classmethod
    def update_token(cls, token=None):
        token_dict = {}
        if token:
            token_dict["authorization"] = "Token " + token
        else:
            cls.graphql_client.base_headers.pop('token', None)
        cls.update_headers(**token_dict)

    # 请求头相关(待测试)
    @classmethod
    def update_headers(cls, **kwargs):
        for key, value in kwargs.items():
            cls.headers[key] = value
            cls.graphql_client.base_headers[key] = value


# 运行 pytest 入口
def run(file_name, maxfail=None):
    pro_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    xml_path = pro_dir + "/output/report/xml/"
    if not maxfail:
        pytest.main(['-q', file_name, '--alluredir', xml_path])
    else:
        pytest.main(['-q', file_name, '-x', '--alluredir', xml_path])
    go_allure()


# 工具函数
def collection():
    ssl._create_default_https_context = ssl._create_unverified_context


def login(account, password):
    url = config.get_web_information('url')
    variables = {'input': {"account": account, "password": password}}
    query = graphql_query.login
    client = HTTPEndpoint(url)
    result = client(query, variables)
    token = jsonpath.jsonpath(result, "$..token")[0]
    return token


if __name__ == "__main__":
    test = BaseTestCase()
    test.assertEqual(None, 100)
