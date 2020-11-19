from support import *
import pytest
import allure

collection()


@allure.epic("thingMaintenance")
@allure.feature("updateThingMaintenance")
class TestUpdateThingMaintenance(BaseTestCase):
    query_name = "updateThingMaintenance"
    interface = GraphqlInterface(query_name)

    create_name = "createThingMaintenance"

    @staticmethod
    def change_input(variable):
        if variable.get("input").get("period").get("type"):
            variable["input"]["period"]["type"] = "SINGLE"
        if variable.get("input").get("period").get("endAt"):
            variable["input"]["period"].pop("endAt")
        if variable.get("input").get("period").get("frequency"):
            variable["input"]["period"].pop("frequency")

    @allure.story("所有项完整")
    def test_1(self, variable, resource, create_id):
        self.all_param.update({"delay": 0.2})
        variable = next(self.interface.generate("generate_all_params", **BaseTestCase.all_param))
        self.change_input(variable)
        # 创建一个id以修改
        _id, _ = create_id(self.create_name, 1, "ThingMaintenance", return_type="variable")
        variable['input']["id"] = _id
        # 使用创建的id
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertForm(variable, result)

    @allure.story("不填写选填项")
    def test_2(self, variable, resource, create_id):
        self.all_param.update({"delay": 0.2})
        variable = next(self.interface.generate("generate_all_params", **BaseTestCase.all_param))
        self.change_input(variable)
        # 创建一个id以修改
        _id, _ = create_id(self.create_name, 1, "ThingMaintenance", return_type="variable")
        variable['input']["id"] = _id
        # 使用创建的id
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertForm(variable, result)


if __name__ == "__main__":
    run(__file__)
