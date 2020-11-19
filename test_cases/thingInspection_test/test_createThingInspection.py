from support import *
import pytest
import allure
import time

collection()


@allure.epic("thingInspection")
@allure.feature("createThingInspection")
class TestCreateThingInspection(BaseTestCase):
    query_name = "createThingInspection"
    interface = GraphqlInterface(query_name)

    @staticmethod
    def change_input(variable):
        if variable.get("input", {}).get("period", {}).get("type", {}):
            variable["input"]["period"]["type"] = "SINGLE"
        if variable.get("input", {}).get("period", {}).get("endAt", {}):
            variable["input"]["period"].pop("endAt")
        if variable.get("input", {}).get("period", {}).get("frequency", {}):
            variable["input"]["period"].pop("frequency")

    @allure.story("所有项完整")
    @pytest.mark.parametrize("variable", interface.generate("generate_all_params", **BaseTestCase.all_param))
    def test_1(self, variable, resource):
        self.change_input(variable)
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertForm(variable, result)

    @allure.story("不填写选填项")
    @pytest.mark.parametrize("variable", interface.generate("generate_no_optional_params", **BaseTestCase.all_param))
    def test_2(self, variable, resource):
        self.change_input(variable)
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertForm(variable, result)

    @allure.story("测试定时任务")
    @pytest.mark.parametrize("variable", interface.generate("generate_all_params", **BaseTestCase.all_param))
    def test_3(self, variable, resource):
        self.change_input(variable)
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertJsonResponseEqual("$..status", result, "INPROGRESS")

    @allure.story("测试定时任务2-延迟启动")
    def test_4(self, resource):
        self.all_param.update({"delay": 0.2})
        variable = next(self.interface.generate("generate_all_params", **self.all_param))
        self.change_input(variable)
        user = resource.simple_user
        result = user.send_request(self.query_name, variable)
        _id = result.find_result("$.." + self.query_name + ".id")[0]
        # 延迟启动前状态为待保养
        self.assertJsonResponseEqual("$..status", result.result, "PENDING")
        # 启动后状态为保养中
        time.sleep(12)
        result = user.send_request("thingInspection", {"id": _id}).result
        self.assertJsonResponseEqual("$..status", result, "INPROGRESS")


if __name__ == "__main__":
    run(__file__)
