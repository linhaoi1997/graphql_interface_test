from support import *
import pytest
import allure

collection()


@allure.epic("sparePart")
@allure.feature("exportSpareParts")
class TestQueryExportSpareParts(BaseTestCase):
    query_name = "exportSpareParts"
    interface = GraphqlInterface(query_name)

    create_name = "createSparePart"
    resource_name = "SparePart"

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
