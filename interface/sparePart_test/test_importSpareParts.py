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
# class TestImportSpareParts(BaseTestCase):
#     query = graphql.get_query("mutations", "importSpareParts")
#     test_right_data = [
#         ['备件导入-只填写必填项.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
#     ]
#
#     @pytest.fixture(scope="function")
#     def import_spare_parts(self, request, resource):
#         variables = request.param
#         self.login("admin", "admin")
#         files = {
#             "operations": (
#                 None, json.dumps({"query": self.query, "variables": {"file": None}, "operationName": "importSpareParts"})),
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
#     @allure.story("import spare_part success")
#     @pytest.mark.parametrize("import_spare_parts", test_right_data, indirect=True)
#     def test_right(self, import_spare_parts):
#         result, _ = import_spare_parts
#         record(result)
#         self.assertCorrect(result)
#
#     # @allure.story("import thing error")
#     # @pytest.mark.parametrize("import_things", test_error_data, indirect=True)
#     # def test_error(self, import_things):
#     #     result, _ = import_things
#     #     record(result)
#     #     self.assertError(result)
#
#
# if __name__ == "__main__":
#     run(__file__)
