# from support import *
# import pytest
# import allure
# import json
# from urllib3 import encode_multipart_formdata
# import requests
#
# collection()
#
#
# @allure.epic("thing")
# @allure.feature("importThings")
# class TestImportThings(BaseTestCase):
#     query = graphql_query.get_query("mutations", "importThings")
#     test_right_data = [
#         ['只有必填项.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['所有项齐全.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         # ['测试用类型1.xls', "	application/vnd.ms-excel"],
#         # ['测试类型用2.xls', "	application/vnd.ms-excel"],
#         # ['测试类型用3.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['5000行.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['更新数据库信息.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#
#     ]
#
#     test_error_data = [
#         # ['空数据.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['必填项为空1.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['必填项为空2.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['必填项为空3.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['不支持的文件类型.pdf', 'application/pdf'],
#         # ['5000行错误.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         # ['重复行.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         # ['设备类型不存在.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#
#     ]
#
#     test_make_import_data = [
#
#         ['只有必填项.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['所有项齐全.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['测试用类型1.xls', "	application/vnd.ms-excel"],
#         ['测试类型用2.xls', "	application/vnd.ms-excel"],
#         ['测试类型用3.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         # ['5000行.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['空数据.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['必填项为空1.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['必填项为空2.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['必填项为空3.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['更新数据库信息.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#         ['不支持的文件类型.pdf', 'application/pdf'],
#
#     ]
#
#     @pytest.fixture(scope="function")
#     def import_things(self, request, resource):
#         variables = request.param
#         self.login("admin", "admin")
#         files = {
#             "operations": (
#                 None, json.dumps({"query": self.query, "variables": {"file": None}, "operationName": "importThings"})),
#             "map": (None, json.dumps({"1": ["variables.file"]})),
#             "1": (variables[0], find_test_file(variables[0]), variables[1])
#         }
#         encode_data = encode_multipart_formdata(files)
#         variables = encode_data[0]
#         # record(variables)
#         self.update_headers(**{"Content-Type": encode_data[1]})
#         record(self.headers)
#         record(variables)
#         return requests.post(self.base_url, headers=self.headers, data=variables).json(), request.param
#
#     @allure.story("import thing success")
#     @pytest.mark.parametrize("import_things", test_right_data, indirect=True)
#     def test_right(self, import_things):
#         result, _ = import_things
#         record(result)
#         self.assertCorrect(result)
#
#     @allure.story("import thing error")
#     @pytest.mark.parametrize("import_things", test_error_data, indirect=True)
#     def test_error(self, import_things):
#         result, _ = import_things
#         record(result)
#         self.assertError(result)
#
#
# if __name__ == "__main__":
#     run(__file__)
