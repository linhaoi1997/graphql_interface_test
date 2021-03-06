from .tools import *
from .tools.find_gralhql_schema import graphql_query
from .caps.read_yaml import config
from .db_fixture.init_data import init_data, PostgresConn
from .base_test.base_api.BaseTest import BaseTestCase, run, collection, AssertMethod
from .base_test.base_api.BaseApi import BaseApi
from .base_test.base_api.SpecialApi import FormStructApi, UploadApi
from .base_test import resource, GraphqlInterface
from support.base_test.GraphqlClient import GraphqlClient

# 这里主要为工具支持函数


__all__ = ["Decorator", "AutoTestLog", "go_allure", "record", "pformat", "create_num_string",
           "init_data", "find_test_file", "create_timestamp",
           "get_all_deepest_dict", "format_number", "BaseTestCase", "run", "collection",
           "find_return_type", "AssertMethod", "GraphqlClient",
           "resource", "GraphqlInterface", "graphql_query", "config", "PostgresConn",
           "BaseApi", "FormStructApi", "UploadApi"
           ]

if __name__ == "__main__":
    go_allure(True)
