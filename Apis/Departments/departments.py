from support.base_test.base_api.SpecialApi import QueryManyApi


class Departments(QueryManyApi):
    def __init__(self, user=None):
        super(Departments, self).__init__("departments", user)


class WorkShops(QueryManyApi):
    def __init__(self, user=None):
        super(WorkShops, self).__init__("workshops", user)

    def query_and_return_ids(self, offset=0, limit=10, _filter=None):
        self.query(offset, limit, _filter)
        return self.find_from_result("$..id")
