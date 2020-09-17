from support import *
import pytest
import allure

collection()


@allure.epic("sparePartReceipt")
@allure.feature("deleteSparePartReceipts")
class TestDeleteSparePartReceipts(BaseTestCase):
    query_name = "deleteSparePartReceipts"
    interface = GraphqlInterface(query_name)

    create_name = "createSparePartReceipt"
    resource_name = "SparePartReceipt"

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
