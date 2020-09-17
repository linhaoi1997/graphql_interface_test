from support import *
import json
import pytest
import allure
import requests
from urllib3 import encode_multipart_formdata

collection()


@allure.epic("file")
@allure.feature("uploadFile")
class TestUploadFile(BaseTestCase):
    query = "mutation uploadFiles($files: [Upload!]!) {\n  uploadFiles(files: $files) {\n    id\n    name\n    url\n    __typename\n  }\n}\n"

    test_right_data = [
        ['052420205956.jpg', 'image/jpg'],
        ['052420205957.jpg', 'image/jpg'],
        ['052420205958.jpg', 'image/jpg'],
        ['052420205959.jpg', 'image/jpg'],
        ['052420205960.jpg', 'image/jpg'],
        ['052420205961.jpg', 'image/jpg'],
        ['052420205962.jpg', 'image/jpg'],
        ['052420205963.jpg', 'image/jpg'],
        ['052420205964.jpg', 'image/jpg'],
        ['052420205965.jpg', 'image/jpg'],
        ['052420205966.jpg', 'image/jpg'],
        ['052420205966.jpg', 'image/jpg'],
        ['test.jpeg', 'image/jpg'],
        ['test0.jpeg', 'image/jpg'],
        ['test0.jpg', 'image/jpg'],
        ['test_change.jpg', 'image/jpg'],
    ]

    @pytest.fixture(scope="function")
    def upload_file(self, request):
        variables = request.param
        files = {
            "operations": (
                None, json.dumps({"query": self.query, "variables": {"file": None}, "operationName": "uploadFile"})),
            "map": (None, json.dumps({"1": ["variables.file"]})),
            "1": (variables[0], find_test_file(variables[0]), variables[1])
        }
        encode_data = encode_multipart_formdata(files)
        variables = encode_data[0]
        # logger.debug(variables)
        self.update_headers(**{"Content-Type": encode_data[1]})
        logger.debug(self.headers)
        return requests.post(self.base_url, headers=self.headers, data=variables).json(), request.param

    @allure.story("upload_file success")
    @pytest.mark.parametrize("upload_file", test_right_data, indirect=True)
    def test_add_right(self, upload_file):
        result, _ = upload_file
        logger.debug(pformat(result))
        self.assertJsonResponseIn("$..id", result)
        self.assertJsonResponseEqual("$..name", result, _[0])


if __name__ == "__main__":
    run(__file__)
