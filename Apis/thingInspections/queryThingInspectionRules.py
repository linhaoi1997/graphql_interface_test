from support.base_test.base_api.SpecialApi import QueryManyApi, QuerySingleApi
import random


class QueryThingInspectionRules(QueryManyApi):

    def __init__(self, user=None):
        super(QueryThingInspectionRules, self).__init__("thingInspectionRules", user)

    def return_random_Rule(self):
        ids = self.query_and_return_ids()
        _id = random.choice(ids)
        return QueryThingInspectionRule().query_and_return_items(_id)


class QueryThingInspectionRule(QuerySingleApi):

    def __init__(self, user=None):
        super(QueryThingInspectionRule, self).__init__("thingInspectionRule", user)

    def query_and_return_items(self, _id):
        self.query(_id)
        rule = self.result["data"][self.api_name]
        return InspectionRule(rule["id"], rule["items"])


class InspectionRule(object):
    def __init__(self, _id, items: list):
        self.id = _id
        self.sub_items = []
        for item in items:
            for sub_item in item["subItems"]:
                self.sub_items.append(SubItem(
                    sub_item.get("id"),
                    sub_item.get("category"),
                    sub_item.get("criteria"),
                    sub_item.get("boundary")
                ))

    def __repr__(self):
        return "rule %s: \n" % self.id + str(self.sub_items)


class SubItem(object):
    NORMAL = "NORMAL"
    NUMBER = "NUMBER"

    def __init__(self, _id, category, criteria=None, boundary=None):
        self.id = _id
        self.category = category
        self.criteria = criteria
        self.boundary = boundary

    def __repr__(self):
        return str((self.id, self.category, self.criteria, self.boundary))


if __name__ == '__main__':
    test = QueryThingInspectionRules()
    print(test.return_random_Rule())
