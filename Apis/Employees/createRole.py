from support import BaseApi
from Apis.Employees.permissions import Permissions


class CreateRole(BaseApi):
    def __init__(self, user=None):
        super(CreateRole, self).__init__("createRole", user)

    def create_role(self, name, permissions_name: list):
        variables = {
            "name": name,
            "permissions": [Permissions().search_permission_id(i) for i in permissions_name]
        }
        return self.run()

    def init_roles(self):
        self.create_role(
            "发起人", [
                "查看主设备列表、详情",
                "查看备件列表、详情",
                "查看备件库存、入库记录、申领记录",
                "查看维修单",
                "发起维修单"
                "查看巡检方案",
                "查看巡检单",
                "发起巡检单",
                "查看保养方案",
                "查看保养单",
                "发起保养单",
                "查看组织架构及人员"
            ]
        )
        self.create_role(
            "执行人", [
                "查看主设备列表、详情",
                "查看备件列表、详情",
                "查看备件库存、入库记录、申领记录",
                "查看维修单",
                "反馈维修单"
                "查看巡检方案",
                "查看巡检单",
                "反馈巡检单",
                "查看保养方案",
                "查看保养单",
                "反馈保养单",
                "查看组织架构及人员"
            ]
        )
        self.create_role(
            "审核人", [
                "查看主设备列表、详情",
                "查看备件列表、详情",
                "查看备件库存、入库记录、申领记录",
                "查看维修单",
                "审核维修单"
                "查看巡检方案",
                "查看巡检单",
                "审核巡检单",
                "查看保养方案",
                "查看保养单",
                "审核保养单",
                "查看组织架构及人员"
            ]
        )
        self.create_role(
            "test", [
                "查看主设备列表、详情",
                "查看备件列表、详情",
                "查看备件库存、入库记录、申领记录"
            ]
        )


if __name__ == '__main__':
    test = CreateRole()
    test.create_role("test", ['查看主设备列表、详情', "导入、导出主设备详情"])
