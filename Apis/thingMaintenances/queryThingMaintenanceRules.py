from support.base_test.base_api.SpecialApi import QueryManyApi, QuerySingleApi
import random


class QueryThingMaintenanceRules(QueryManyApi):
    def __init__(self, user=None):
        super(QueryThingMaintenanceRules, self).__init__("thingMaintenanceRules", user)

    def return_random_rule(self):
        ids = self.query_and_return_ids()
        _id = random.choice(ids)
        return QueryThingMaintenanceRule(self.user).query_and_return_items(_id)


class QueryThingMaintenanceRule(QuerySingleApi):

    def __init__(self, user=None):
        super(QueryThingMaintenanceRule, self).__init__("thingMaintenanceRule", user)

    def query_and_return_items(self, _id):
        self.query(_id)
        rule = self.result["data"][self.api_name]
        return MaintenanceRule(rule["id"], rule["items"])


class MaintenanceRule(object):
    def __init__(self, _id, items_list: list):
        self.id = _id
        self.sub_items = []
        for item in items_list:
            self.sub_items.append(MaintenanceSubItem(item["id"], item["name"]))


class MaintenanceSubItem(object):
    def __init__(self, _id, name):
        self.id = _id
        self.name = name
