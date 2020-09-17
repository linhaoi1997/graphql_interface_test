from support import *
import pytest
import allure

collection()


@allure.epic("department")
@allure.feature("updateDepartment")
class TestUpdateDepartment(BaseTestCase):
    query_name = "updateDepartment"
    interface = GraphqlInterface(query_name)

    create_name = "createDepartment"
    resource_name = "Department"

    @allure.story("所有项完整")
    @pytest.mark.parametrize("variable", interface.generate("generate_all_params", **BaseTestCase.all_param))
    def test_1(self, variable, resource, create_id):
        # 创建一个id以修改
        _id, _ = create_id(self.create_name, 1, self.resource_name, return_type="variable")
        variable['input']["id"] = _id
        # 使用创建的id
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        _id = variable["input"].pop("parent")
        self.assertForm(variable, result)
        assert str(_id["id"]) in result["data"]["updateDepartment"]["parentPath"]


if __name__ == "__main__":
    run(__file__)
