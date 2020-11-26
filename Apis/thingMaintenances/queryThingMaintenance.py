from support.base_test.base_api.SpecialApi import QuerySingleApi, QueryManyApi


class QueryMaintenance(QuerySingleApi):
    def __init__(self, _id=None, user=None):
        super(QueryMaintenance, self).__init__("thingMaintenance", user)
        self.id = _id

    def query_and_find_status(self):
        self.query(self.id)
        return self.find_first_deep_item("status")


class QueryMaintenances(QueryManyApi):

    def __init__(self, user=None):
        super(QueryMaintenances, self).__init__("thingMaintenances", user)

    def query_and_return_first_id(self):
        return self.query_and_return_ids()[0]
