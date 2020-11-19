from support import *
import pytest
import allure

collection()


@allure.epic("sparePart")
@allure.feature("deleteSpareParts")
class TestDeleteSpareParts(BaseTestCase):
    query_name = "deleteSpareParts"
    interface = GraphqlInterface(query_name)

    create_name = "createSparePart"
    resource_name = "SparePart"

    @allure.story("删除3个")
    def test_1(self, resource, create_id):
        _ids = create_id(self.create_name, 3, self.resource_name)

        variable = {
            "input": {"ids": _ids}
        }
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertDelete(variable, result)


if __name__ == "__main__":
    run(__file__)
