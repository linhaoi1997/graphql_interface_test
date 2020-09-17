from support import *
import pytest
import allure

collection()


@allure.epic("thingInspection")
@allure.feature("queryThingInspection")
class TestQueryThingInspection(BaseTestCase):
    query_name = "thingInspection"
    interface = GraphqlInterface(query_name)

    create_name = "createThingInspection"
    resource_name = "ThingInspection"

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
