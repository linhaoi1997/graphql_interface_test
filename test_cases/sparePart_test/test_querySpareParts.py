from support import *
import pytest
import allure

collection()


@allure.epic("sparePart")
@allure.feature("querySpareParts")
class TestQuerySpareParts(BaseTestCase):
    query_name = "spareParts"
    interface = GraphqlInterface(query_name)

    create_name = "createSparePart"
    resource_name = "SparePart"

    @allure.story("正确查询")
    def test_query_thing(self, resource, create_id):
        _ids = create_id(self.create_name, 3, self.resource_name, return_type="id")
        user = resource.simple_user
        variables = {"offset": 0, "limit": 3, "filter": {}}  # 分页查询一个
        result = user.send_request(self.query_name, variables).result
        self.assertQuerys(_ids, result)


if __name__ == "__main__":
    run(__file__)
