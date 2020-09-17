from support import *
import pytest
import allure

collection()


@allure.epic("thingMaintenanceRule")
@allure.feature("updateThingMaintenanceRule")
class TestUpdateThingMaintenanceRule(BaseTestCase):
    query_name = "updateThingMaintenanceRule"
    interface = GraphqlInterface(query_name)

    create_name = "createThingMaintenanceRule"
    resource_name = "ThingMaintenanceRule"

    @allure.story("所有项完整")
    @pytest.mark.parametrize("variable", interface.generate("generate_all_params", **BaseTestCase.all_param))
    def test_1(self, variable, resource, create_id):
        # 创建一个id以修改
        _id, _id_map = create_id(self.create_name, 1, self.resource_name, return_type="result")
        variable['input']["id"] = _id
        for i in range(self.all_param.get("list_len")):
            variable['input']['items'][i]["id"] = _id_map['ThingMaintenanceItem'][i]
        # 使用创建的id
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertForm(variable, result)

    @allure.story("不填写选填项")
    @pytest.mark.parametrize("variable", interface.generate("generate_no_optional_params", **BaseTestCase.all_param))
    def test_2(self, variable, resource, create_id):
        # 创建一个id以修改
        _id, _id_map = create_id(self.create_name, 1, self.resource_name, return_type="result")
        variable['input']["id"] = _id
        # 使用创建的id
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertForm(variable, result)


if __name__ == "__main__":
    run(__file__)
