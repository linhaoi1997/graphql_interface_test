from .tools import *
from .caps.read_yaml import get_file_path, get_web_information, get_account
from .db_fixture.init_data import init_data
from .create_graphql_py.interface_writer import InterfaceWriter
from .data_maker.DataMaker import DataMaker, InputSearcher
from .base_test.BaseTest import BaseTestCase, run, collection, AssertMethod
from .base_test import ResourceLoader, GraphqlInterface
from .data_maker.GraphqlClient import GraphqlClient

# 这里主要为工具支持函数


__all__ = ["Decorator", "AutoTestLog", "find_schema", "get_file_path", "go_allure", "logger", "pformat",
           "get_web_information", "create_num_string", "init_data", "find_test_file", "create_timestamp",
           "get_all_deepest_dict", "format_number", "InterfaceWriter", "DataMaker", "InputSearcher",
           "BaseTestCase", "run", "collection", "find_return_type", "AssertMethod", "GraphqlClient",
           "ResourceLoader", "GraphqlInterface", "get_account"
           ]

if __name__ == "__main__":
    go_allure(True)
