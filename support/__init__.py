from .tools import *
from .tools.find_gralhql_schema import graphql_query
from .caps.read_yaml import config
from .db_fixture.init_data import init_data
from .create_graphql_py.interface_writer import InterfaceWriter
from .data_maker.DataMaker import DataMaker, InputSearcher
from support.base_test.base_api.BaseTest import BaseTestCase, run, collection, AssertMethod
from .base_test import ResourceLoader, GraphqlInterface
from .data_maker.GraphqlClient import GraphqlClient

# 这里主要为工具支持函数


__all__ = ["Decorator", "AutoTestLog", "go_allure", "record", "pformat", "create_num_string",
           "init_data", "find_test_file", "create_timestamp",
           "get_all_deepest_dict", "format_number", "InterfaceWriter", "DataMaker", "InputSearcher",
           "BaseTestCase", "run", "collection", "find_return_type", "AssertMethod", "GraphqlClient",
           "ResourceLoader", "GraphqlInterface", "graphql_query", "config"
           ]

if __name__ == "__main__":
    go_allure(True)
