from support import *
from support.base_test.ResourceLoader import ResourceLoader
from beeprint import pp
import pytest
import allure
import jsonpath

collection()

resource = ResourceLoader()


@allure.epic("Role")
@allure.feature("test Permission")
class TestPermission(BaseTestCase):
    # 查出所有权限表，为每种小权限添加一种角色,为每个角色创建一个员工
    # init_data()
    variables = []
    query_name = "permissionTable"
    variable = {}
    user = resource.test_user
    num = 1
    result = user.send_request(query_name, variable).result["data"]["permissionTable"]["modules"]
    for module in result:
        variable = {
            "input": {"name": module["name"],
                      "permissions": [{"id": i} for i in jsonpath.jsonpath(module, "permissions[*].id")]}}
        query_name = "createRole"
        __id = user.send_request(query_name, variable).find_id()
        # 创建员工
        query_name = "createEmployee"
        variable = {
            "input": {
                "name": module["name"],
                "department": {"id": 1},
                "code": create_num_string(5),
                "phone": "123456",
                "account": "admin" + str(num),
                "password": "123456",
                "status": "ACTIVATED",
                "roles": [{"id": __id}]
            }
        }
        num += 1
        result = user.send_request(query_name, variable)
        try:
            result = result.find_id()
            variables.append(
                {
                    "login": {
                        "account": variable["input"]["account"],
                        "password": variable["input"]["password"],
                    },
                    "interfaces": module["name"]
                }
            )
        except Exception as e:
            record(e)

    def test(self):
        record(self.variables)
    # @pytest.mark.parametrize("variable", variables)
    # def test_permission(self, variable):
    #     user = resource.test_user
    #     user.login(variable["login"])
    #     error_interface = []
    #     for test_cases in variable["interfaces"]:
    #         interface_name = test_cases.split('/')[-1]
    #         try:
    #             query_name = interface_name
    #             test_cases = GraphqlInterface(query_name).generate_params(**self.all_param)
    #             result = user.send_request(query_name, test_cases).result
    #             self.assertError(result)
    #         except Exception as e:
    #             record(e)
    #             error_interface.append(interface_name)
    #     assert not error_interface


if __name__ == '__main__':
    run(__file__)
