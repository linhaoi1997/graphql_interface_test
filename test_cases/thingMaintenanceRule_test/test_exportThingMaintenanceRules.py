from support import *
import pytest
import allure

collection()


@allure.epic("thingMaintenanceRule")
@allure.feature("exportThingMaintenanceRules")
class TestQueryExportThingMaintenanceRules(BaseTestCase):
    query_name = "exportThingMaintenanceRules"
    interface = GraphqlInterface(query_name)

    create_name = "createThingMaintenanceRule"

    @allure.story("导出三项")
    def test(self, resource, create_id):
        _ids = create_id(self.create_name, 3, "ThingMaintenanceRule")

        variable = {
            "input": {"ids": _ids}
        }
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertExport(result)


if __name__ == "__main__":
    run(__file__)
