from support import *
import pytest
import allure

collection()


@allure.epic("Role")
@allure.feature("queryRoles")
class TestQueryRoles(BaseTestCase):
    query_name = "roles"
    interface = find_schema("queries", query_name)

    @allure.story("所有项完整")
    def test_1(self, resource):
        user = resource.simple_user
        variable = {}
        result = user.send_request(self.query_name, variable).result
        self.assertCorrect(result)


if __name__ == "__main__":
    run(__file__)
