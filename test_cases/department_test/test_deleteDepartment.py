from support import *
import pytest
import allure

collection()


@allure.epic("department")
@allure.feature("deleteDepartment")
class TestDeleteDepartment(BaseTestCase):
    query_name = "deleteDepartment"
    interface = GraphqlInterface(query_name)

    create_name = "createDepartment"
    resource_name = "Department"

    @allure.story("删除1个")
    def test_1(self, resource, create_id):
        _ids = create_id(self.create_name, 1, self.resource_name)

        variable = {
            "department": {"id": _ids[0]}
        }
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertJsonResponseEqual("$..deleteDepartment", result, True)


if __name__ == "__main__":
    run(__file__)
