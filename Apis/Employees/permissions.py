from support import BaseApi


class Permissions(BaseApi):
    def __init__(self, user=None):
        super(Permissions, self).__init__("permissionTable", user)
        self.run()
        self.permission = []
        # print(self.result)
        for permissions in self.result.get("data").get("permissionTable").get("modules"):
            for permission in permissions["permissions"]:
                self.permission.append(Permission(permission["description"], permission["id"]))

    def search_permission(self, description):
        for permission in self.permission:
            if permission.description == description:
                return permission
        else:
            raise Exception("NO FOUND PERMISSION")

    def search_permission_id(self, permission_name):
        return self.search_permission(permission_name).id


class Permission(object):
    def __init__(self, description, _id):
        self.description = description
        self.id = _id


if __name__ == '__main__':
    test = Permissions()
    test_permission = test.search_permission("导入、导出主设备详情")
    print(test_permission.description)
    print(test_permission.id)
