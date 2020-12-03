from support.base_test.base_api.SpecialApi import QueryManyApi, QuerySingleApi
import random


class Things(QueryManyApi):
    def __init__(self, user=None):
        super(Things, self).__init__("things", user)

    def run_and_query_id(self, variables):
        self.run(variables)
        return self.find_from_result("$..data[*].id")[0]

    def search(self, search_str):
        variables = {
            "filter": {
                "search": search_str
            }
        }
        return self.run_and_query_id(variables)

    def filter_by_field(self, field_id, values=None):
        if values is None:
            values = []
        variables = {
            "field": {
                "id": field_id
            },
            "values": values
        }
        return self.run_and_query_id(variables)

    def return_random_thing(self):
        return random.choice(self.query_and_return_ids())


class Thing(QuerySingleApi):
    def __init__(self, user=None):
        super(Thing, self).__init__("thing", user)

    def query_and_return_contact_ids(self, _id):
        self.query(_id)
        return self.find_from_result("$.data."+self.api_name+".repairContacts[*].id")


if __name__ == '__main__':
    test = Things()
    print(test.search("name"))
