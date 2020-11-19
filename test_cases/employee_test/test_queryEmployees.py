from support import *
import pytest
import allure

collection()


@allure.epic("employee")
@allure.feature("queryEmployees")
class TestQueryEmployees(BaseTestCase):
    query_name = "employees"
    interface = GraphqlInterface(query_name)

    create_name = "createEmployee"
    resource_name = "Employee"

    @allure.story("正确查询")
    def test_query_thing(self, resource, create_id):
        _ids = create_id(self.create_name, 3, self.resource_name, return_type="id")
        user = resource.simple_user
        variables = {"offset": 0, "limit": 3,
                     "filter": {"department": {"id": 1}, "containSubsidiaries": True},
                     "orderBy": ["+updated_at"]
                     }  # 分页查询一个
        result = user.send_request(self.query_name, variables).result
        self.assertQuerys(_ids, result)


if __name__ == "__main__":
    run(__file__)
