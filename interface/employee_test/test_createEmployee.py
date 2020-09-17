from support import *
import pytest
import allure

collection()


@allure.epic("employee")
@allure.feature("createEmployee")
class TestCreateEmployee(BaseTestCase):
    query_name = "createEmployee"
    interface = GraphqlInterface(query_name)

    @allure.story("所有项完整")
    @pytest.mark.parametrize("variable", interface.generate("generate_all_params", **BaseTestCase.all_param))
    def test_1(self, variable, resource):
        variable["input"]["email"] = "test@sina.com"
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        variable["input"].pop("password")
        self.assertForm(variable, result)

    @allure.story("不填写选填项")
    @pytest.mark.parametrize("variable", interface.generate("generate_no_optional_params", **BaseTestCase.all_param))
    def test_2(self, variable, resource):
        variable["input"]["email"] = "test@sina.com"
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        variable["input"].pop("password")
        self.assertForm(variable, result)


if __name__ == "__main__":
    run(__file__)
