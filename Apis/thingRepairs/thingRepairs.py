from support.base_test.base_api.SpecialApi import QueryManyApi


class QueryThingRepairs(QueryManyApi):
    def __init__(self, user=None):
        super(QueryThingRepairs, self).__init__("thingRepairs", user)

    def run_and_query_id(self, variables=None):
        if not variables:
            variables = {"offset": 0, "limit": 10, "filter": {}}
        self.run(variables)
        return self.find_from_result("$..data[*].id")[0]
