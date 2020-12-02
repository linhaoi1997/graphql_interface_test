from support.base_test.base_api.SpecialApi import UpdateApi
from Apis.Employees.permissions import Permissions
from Apis.Employees.Role import Roles


class UpdateRole(UpdateApi):

    def __init__(self, user=None, _id=None):
        super(UpdateRole, self).__init__("updateRole", user)
        self.id = _id

    def add_permission(self, permission_name_list: list):
        permissions = Roles.query_role(self.id)
        add_permissions_list = [Permissions().search_permission_id(i) for i in permission_name_list]
        permissions.extend(add_permissions_list)
        var = {
            "permissions": [{"id": i} for i in permissions]
        }
        return self.update(variables=var)
