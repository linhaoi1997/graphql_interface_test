from support import *
import json
import pytest
import allure
import requests
from urllib3 import encode_multipart_formdata

collection()
resource = ResourceLoader()


@allure.epic("file")
@allure.feature("uploadFile")
class TestUploadFile(BaseTestCase):
    query = "mutation uploadFiles($files: [Upload!]!) {\n  uploadFiles(files: $files) {\n    id\n    name\n    url\n    __typename\n  }\n}\n"
    test_right_data = [
        ['test.jpg', 'image/jpg'],  # id=2,5,6
        ['test2.jpeg', 'image/jpg'],
        ['test3.jpeg', 'image/jpg'],
        ['test.pdf', 'application/pdf'],
        ['test.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        ['doc文件.doc', "application/msword"],
        ['image.png', "application/msword"],

        # ['text.xls', 'application/vnd.ms-excel']
    ]

    test_make_import_data = [

        ['只有必填项.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        ['所有项齐全.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        ['测试用类型1.xls', "	application/vnd.ms-excel"],
        ['测试类型用2.xls', "	application/vnd.ms-excel"],
        ['测试类型用3.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        ['5000行.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        ['空数据.xls', "	application/vnd.ms-excel"],
        ['必填项为空1.xlsx', "application/vnd.ms-excel"],
        ['必填项为空2.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        ['必填项为空3.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        ['更新数据库信息.xlsx', "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
        ['不支持的文件类型.pdf', 'application/pdf'],

    ]

    @pytest.fixture(scope="function")
    def upload_file(self, request):
        variables = request.param
        files = {
            "operations": (
                None,
                json.dumps({"query": self.query, "variables": {"files": [None]}, "operationName": "uploadFiles"})),
            "map": (None, json.dumps({"1": ["variables.files.0"]})),
            "1": (variables[0], find_test_file(variables[0]), variables[1])
        }
        self.login("admin_jia", "123456")
        encode_data = encode_multipart_formdata(files)
        data = encode_data[0]
        # record(variables)
        self.update_headers(**{"Content-Type": encode_data[1]})
        record(self.headers)
        record(self.query)
        return requests.post(self.base_url, headers=self.headers, data=data).json(), request.param

    @allure.story("upload_file success")
    @pytest.mark.parametrize("upload_file", test_right_data, indirect=True)
    def test_add_right(self, upload_file):
        result, _ = upload_file
        record(pformat(result))
        self.assertJsonResponseIn("$..id", result)
        self.assertJsonResponseEqual("$..name", result, _[0])

    @allure.story("upload_file make import data")
    @pytest.mark.parametrize("upload_file", test_make_import_data, indirect=True)
    def test_import_right(self, upload_file):
        result, _ = upload_file
        record(pformat(result))


if __name__ == "__main__":
    run(__file__)
