from support.base_test.generate_param.newSchema import base_schema, Schema
from support.base_test.generate_param.GenerateParam import GraphqlInterface
from support.base_test.ResourceLoader import resource
from support.base_test.JsonSetter import JsonSetter
import jsonpath


class BaseApi(object):
    def __init__(self, api_name, user=None, schema: Schema = base_schema):
        self.schema = schema
        self.api_name = api_name
        if user:
            self.user = user
        else:
            self.user = resource.simple_user
        self.interface_generator = GraphqlInterface(api_name, schema)
        self.variables = self.interface_generator.generate_params(is_random=True)
        self.result = None
        self.id = None

    # 发送接口方法
    def random_run(self):
        self.run()
        self.set_random_variables()

    def run(self, variables=None):
        if variables:
            self.variables = variables
        self.result = self.user.send_request(self.api_name, self.variables).result
        return self.result

    # 设置变量方法

    def set_random_variables(self, **kwargs):
        self.variables = self.interface_generator.generate_params(is_random=True, **kwargs)

    def set_no_optional_var(self, **kwargs):
        self.variables = self.interface_generator.generate_params(is_random=True, no_optional=True, no_none=True)

    def pop_value(self, f_json_path):
        test = JsonSetter(f_json_path)
        test.pop(self.variables)

    def change_value(self, f_json_path, value):
        test = JsonSetter(f_json_path)
        test.set(self.variables, value)

    # 查找方法

    def find_from_result(self, json_path):
        return jsonpath.jsonpath(self.result, json_path)

    def find_first_deep_item(self, name):
        json_path = "$.data." + self.api_name + "." + name
        try:
            return jsonpath.jsonpath(self.result, json_path)[0]
        except TypeError:
            raise AssertionError("没有找到值 %s" % json_path)

    @staticmethod
    def return_id_input(_id):
        if isinstance(_id, list):
            return [{"id": i} for i in _id]
        else:
            return {"id": _id}
