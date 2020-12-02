from support.base_test.base_api.SpecialApi import QueryManyApi, QuerySingleApi


class QueryThingRepairs(QueryManyApi):
    def __init__(self, user=None):
        super(QueryThingRepairs, self).__init__("thingRepairs", user)

    def run_and_query_id(self, variables=None):
        if not variables:
            variables = {"offset": 0, "limit": 10, "filter": {}}
        self.run(variables)
        return self.find_from_result("$..data[*].id")[0]


class QueryThingRepair(QuerySingleApi):
    REJECT = "REJECT"
    DISPATCHING = "DISPATCHING"
    REPAIRING = "REPAIRING"
    FEEDBACK = "FEEDBACK"
    FINISHED = "FINISHED"
    STOP = "STOP"

    def __init__(self, user=None):
        super(QueryThingRepair, self).__init__("thingRepair", user)

    def return_thing_repair_status(self, _id):
        self.query(_id)
        return self.find_first_deep_item("status")
