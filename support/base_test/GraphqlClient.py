from support.caps.read_yaml import config
from sgqlc.endpoint.http import HTTPEndpoint
from jsonpath import jsonpath
from support.tools.find_gralhql_schema import graphql_query
from support.tools import record, pformat
import allure


class GraphqlClient(object):

    def __init__(self, login=None):
        self.base_url = config.get_web_information('url')
        self.platform_url = config.get_web_information('platform_url')
        self.headers = {"Content-Type": "application/json"}
        self.graphql_client = HTTPEndpoint(self.base_url, self.headers)
        self.result = None
        self.num = 0
        self.id = None
        if login:
            try:
                self.login(login)
            except Exception as e:
                record(e)
                record(login)
                record("登录错误")

    @allure.step('send request {1}')
    def send_request(self, query_name, variables, has_typename=True):
        query = graphql_query.get_query(query_name, has_typename)
        self.graphql_client.url = self.base_url + "?" + query_name
        result = self.graphql_client(query, variables)
        self.result = result
        try:
            record(self.graphql_client.url, "发送的url")
            record(self.headers, "发送的headers")
            record(pformat(variables), "发送的参数")
            record(pformat(result), "返回的结果")
        except KeyError as e:
            print(e)
        return self

    def update_headers(self, **kwargs):
        for key in kwargs.keys():
            self.headers[key] = kwargs[key]
        self.graphql_client.base_headers = self.headers

    def update_token(self, token=None):
        token_dict = {}
        if token:
            token_dict["authorization"] = "Token " + token
        else:
            self.graphql_client.base_headers.pop('authorization', None)
        self.update_headers(**token_dict)

    def find_result(self, json_path):
        find = jsonpath(self.result, json_path)
        return find

    def find_id(self):
        return self.find_result("$..id")[0]

    def find_all_id(self, result=None):
        # 遍历返回json所有层以查找返回的所有id
        if not result:
            result = self.result
        if isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, dict):
                    yield from self.find_all_id(value)
                elif isinstance(value, list):
                    for sub_value in value:
                        yield from self.find_all_id(sub_value)
                elif "id" == key:
                    yield result["__typename"], result['id']

    @allure.step("登录 {1}")
    def login(self, login_information):
        account, password = login_information.values()
        variables = {"input": {"account": account, "password": password}}
        token = self.send_request("login", variables).find_result("$..token")[0]
        self.update_token(token)

    def __call__(self, query, variables):
        self.send_request(query, variables)
        return self
