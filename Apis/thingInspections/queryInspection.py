from support.base_test.base_api.SpecialApi import QuerySingleApi


class QueryInspection(QuerySingleApi):

    def __init__(self, user=None, _id=None):
        super(QueryInspection, self).__init__("thingInspection", user)
        self.id = _id

    def query_and_find_status(self):
        self.query(self.id)
        return self.find_first_deep_item("status")
