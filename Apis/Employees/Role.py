from support.base_test.base_api.SpecialApi import QueryManyApi
import jsonpath


class Roles(QueryManyApi):
    def __init__(self, user=None, _id=None):
        super(Roles, self).__init__("roles", user)
        self.id = _id

    def query_role(self, _id=None):
        if not _id:
            _id = self.id
        self.query(_id)
        for role in self.result["data"][self.api_name]:
            if role["id"] == _id:
                return jsonpath.jsonpath(role, "$.permissions[*].id")
        raise Exception("没找到角色")


class Employees(QueryManyApi):
    def __init__(self, user=None):
        super(Employees, self).__init__("employees", user)


if __name__ == '__main__':
    test = Roles()
    print(test.query_role("1"))
