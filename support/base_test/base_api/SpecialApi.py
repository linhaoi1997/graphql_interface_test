from support.base_test.base_api.BaseApi import BaseApi
from support.tools import graphql_query, find_test_file, logger
import json
import requests
from urllib3 import encode_multipart_formdata


def format_s(name: str):
    if name.endswith("s"):
        return name[:-1]
    return name


def format_name(name: str):
    all_name = (
        "spare_part_outbounds", "spare_part_receipts", "spare_parts", "thing_inspection_rules",
        "thing_inspections", "thing_inspections_feedback",
        "thing_maintenance", "thing_maintenance_feedback", "thing_maintenance_rules", "thing_repairs",
        "thing_repairs_feedback", "things"
    )
    if name.endswith("Input"):
        name = name[:-5]
    if name.startswith("Create") or name.startswith("Update"):
        name = name[6:]
    name = name.lower()
    for i in all_name:
        if "".join([format_s(j) for j in i.split("_")]) == name:
            return i
    raise Exception("没有找到对应表单")


class FormStructApi(BaseApi):

    def run(self, is_change_struct=False):
        if is_change_struct:
            self.change_struct()
            self.set_random_variables()
        self.result = self.user.send_request(self.api_name, self.variables).result

    def change_struct(self):
        interface = getattr(self.schema, self.api_name)
        _input = getattr(self.schema, interface.input)
        # 接口查询对应表单的formstruct
        form_struct = BaseApi("formStruct")
        form_struct.variables = {"name": format_name(_input.name), "isDraft": False}
        form_struct.run()
        result = form_struct.result
        custom_fields = result["data"]["formStruct"]["customFields"]
        # 更新api
        _input.update_param(custom_fields, self.schema)


class UploadApi(BaseApi):
    def __init__(self):
        super(UploadApi, self).__init__("uploadFiles")

    def upload(self, files_name: list):
        files_num = len(files_name)
        # operation 的参数
        file_list = [None for i in range(files_num)]
        # map 的参数
        file_dict = {}
        for i in range(files_num):
            file_dict[str(i + 1)] = ["variables.files.%s" % i]
        self.variables = {
            "operations": (
                None,
                json.dumps({"query": graphql_query.get_query(self.api_name),
                            "variables": {"files": file_list},
                            "operationName": "uploadFiles"})),
            "map": (None, json.dumps(file_dict)),
        }
        # 每个file对应的值
        file_map = {}
        for i in range(files_num):
            file_name = files_name[i]
            file_tuple = {str(i + 1): (file_name, find_test_file(file_name), self.get_type(file_name))}
            self.variables.update(**file_tuple)

        encode_data = encode_multipart_formdata(self.variables)
        data = encode_data[0]
        self.user.update_headers(**{"Content-Type": encode_data[1]})
        return requests.post(self.user.base_url, headers=self.user.headers, data=data).json()

    @staticmethod
    def get_type(name: str):
        _type = name.split('.')[-1]
        type_map = {
            'xls': 'application/vnd.ms-excel',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            "pdf": "application/pdf",
            "doc": "application/msword",
            "png": "application/msword",
            "jpg": "image/jpg"
        }
        try:
            return type_map.get(_type)
        except KeyError:
            raise Exception("没有对应类型，请补充")


if __name__ == '__main__':
    test = FormStructApi("createSparePart")
    test.change_struct()
    test = UploadApi()
    print(test.upload(["test.jpg", "test.jpeg"]))
