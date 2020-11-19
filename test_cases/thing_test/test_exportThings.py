from support import *
import pytest
import allure

collection()


@allure.epic("thing")
@allure.feature("exportThings")
class TestQueryExportThings(BaseTestCase):
    query_name = "exportThings"
    interface = GraphqlInterface(query_name)

    create_name = "createThing"
    resource_name = "Thing"

    @allure.story("导出三项")
    def test(self, resource, create_id):
        _ids = create_id(self.create_name, 3, self.resource_name)

        variable = {
            "input": {"ids": _ids}
        }
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertExport(result)


if __name__ == "__main__":
    run(__file__)
