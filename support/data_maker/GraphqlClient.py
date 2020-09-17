from ..caps.read_yaml import get_web_information
from sgqlc.endpoint.http import HTTPEndpoint
from jsonpath import jsonpath
from ..tools.find_gralhql_schema import find_schema, find_test_file
from ..tools import logger, pformat
from urllib3 import encode_multipart_formdata
import json
import requests


class GraphqlClient(object):
    query = {}

    def __init__(self, login=None):
        self.base_url = get_web_information('url')
        self.platform_url = get_web_information('platform_url')
        self.headers = {"Content-Type": "application/json"}
        self.graphql_client = HTTPEndpoint(self.base_url, self.headers)
        self.result = None
        self.num = 0
        if login:
            self.login(login)

    def send_request(self, query_name, variables, is_platform=False, has_typename=True):
        if not self.query.get(query_name):
            try:
                query = find_schema("mutations", query_name, is_platform, has_typename)
            except FileNotFoundError as e:
                # logger.debug(e)
                query = find_schema("queries", query_name, is_platform, has_typename)
            self.query[query_name] = query
        else:
            query = self.query[query_name]
        if not is_platform:
            self.graphql_client.url = self.base_url + "?" + query_name
        else:
            self.graphql_client.url = self.platform_url + "?" + query_name
        logger.debug(self.graphql_client.url)
        logger.debug(self.headers)
        logger.debug(pformat(variables))
        result = self.graphql_client(query, variables)
        self.result = result
        logger.debug(pformat(result))
        return self

    def update_header(self, **kwargs):
        for key in kwargs.keys():
            self.headers[key] = kwargs[key]
        self.graphql_client.base_headers = self.headers

    def update_token(self, token=None):
        token_dict = {}
        if token:
            token_dict["authorization"] = "Token " + token
        else:
            self.graphql_client.base_headers.pop('authorization', None)
        self.update_header(**token_dict)

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

    def login(self, login_information):
        account, password = login_information.values()
        variables = {"input": {"account": account, "password": password}}
        token = self.send_request("login", variables, is_platform=False).find_result("$..token")[0]
        self.update_token(token)

    def __call__(self, query, variables):
        self.send_request(query, variables)
        return self

    def upload_file(self):
        upload_data = [
            ['test.jpg', 'image/jpg'],
            ['test2.jpeg', 'image/jpg'],
            ['test3.jpeg', 'image/jpg'],
        ]
        query = "mutation uploadFiles($files: [Upload!]!) {\n  uploadFiles(files: $files) " \
                "{\n    id\n    name\n    url\n    __typename\n  }\n}\n"
        variables = upload_data[self.num]
        if self.num == len(upload_data):
            self.num = 0
        else:
            self.num += 1
        files = {
            "operations": (
                None,
                json.dumps({"query": query, "variables": {"files": [None]}, "operationName": "uploadFiles"})),
            "map": (None, json.dumps({"1": ["variables.files.0"]})),
            "1": (variables[0], find_test_file(variables[0]), variables[1])
        }
        encode_data = encode_multipart_formdata(files)
        data = encode_data[0]
        self.update_header(**{"Content-Type": encode_data[1]})
        logger.debug(self.headers)
        logger.debug(self.query)
        result = requests.post(self.base_url, headers=self.headers, data=data)
        self.update_header(**{"Content-Type": "application/json"})
        return result["data"]["uploadFiles"]
