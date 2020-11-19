from support import *
import pytest
import allure

collection()


@allure.epic("thing")
@allure.feature("queryThing")
class TestQueryThing(BaseTestCase):
    query_name = "thing"
    interface = GraphqlInterface(query_name)

    create_name = "createThing"
    resource_name = "Thing"

    @allure.story("正确查询")
    def test_query_thing(self, resource, create_id):
        _id, verify_variables = create_id(self.create_name, 1, self.resource_name, return_type="variable")
        user = resource.simple_user
        variables = {
            "id": _id
        }
        result = user.send_request(self.query_name, variables).result
        self.assertForm(verify_variables, result)


if __name__ == "__main__":
    run(__file__)
