from support import *
import pytest
import allure

collection()


@allure.epic("department")
@allure.feature("queryDepartments")
class TestQueryEmployees(BaseTestCase):
    query_name = "departments"
    interface = GraphqlInterface(query_name)

    @allure.story("所有项完整")
    def test_1(self, resource):
        user = resource.simple_user
        variable = {}
        result = user.send_request(self.query_name, variable).result
        self.assertCorrect(result)


if __name__ == "__main__":
    run(__file__)
