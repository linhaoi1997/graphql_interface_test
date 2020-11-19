from support import *
import pytest
import allure

collection()


@allure.epic("thingInspectionRule")
@allure.feature("createThingInspectionRule")
class TestCreateThingInspectionRule(BaseTestCase):
    query_name = "createThingInspectionRule"
    interface = GraphqlInterface(query_name)
    all_param = {
        "list_len": 3,
        "num": 1,
        "is_random": True,
        "no_none": True,
    }

    @allure.story("所有项完整")
    @pytest.mark.parametrize("variable", interface.generate("generate_all_params", **all_param))
    def test_1(self, variable, resource):
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertForm(variable, result)

    @allure.story("不填写选填项")
    @pytest.mark.parametrize("variable", interface.generate("generate_no_optional_params", **all_param))
    def test_2(self, variable, resource):
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertForm(variable, result)


if __name__ == "__main__":
    run(__file__)
