from support import *
import pytest
import allure

collection()


@allure.epic("Role")
@allure.feature("createRole")
class TestCreateRole(BaseTestCase):
    query_name = "createRole"
    interface = GraphqlInterface(query_name)

    @allure.story("所有项完整")
    @pytest.mark.parametrize("variable", interface.generate_all_params(**BaseTestCase.all_param))
    def test_1(self, variable, resource):
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertForm(variable, result)

    @allure.story("不填写选填项")
    @pytest.mark.parametrize("variable", interface.generate_no_optional_params(**BaseTestCase.all_param))
    def test_2(self, variable, resource):
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertForm(variable, result)


if __name__ == "__main__":
    run(__file__)
