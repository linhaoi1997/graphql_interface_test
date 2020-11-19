from support import *
from support.base_test.ResourceLoader import ResourceLoader
from beeprint import pp
import pytest
import allure

collection()

resource = ResourceLoader()


@allure.epic("Role")
@allure.feature("test all Permission")
class TestPermission(BaseTestCase):
    # 查出所有权限表，为每种小权限添加一种角色,为每个角色创建一个员工
    query_name = "permissionTable"

    def test_all_permission(self):
        variable = {}
        user = resource.test_user
        result = user.send_request(self.query_name, variable).result["data"]["permissionTable"]["modules"]
        scopes = []
        for permission in result:
            for interface in permission["permissions"]:
                scopes.extend([i.split('/')[-1] for i in interface["scopes"]])
        un_use_interfaces = []
        for i in resource.all:
            if i not in scopes:
                un_use_interfaces.append(i)
        print(un_use_interfaces)
        record(un_use_interfaces)
        # assert un_use_interfaces == []


if __name__ == '__main__':
    run(__file__)
