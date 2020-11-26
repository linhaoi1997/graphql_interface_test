from support.base_test.base_api.SpecialApi import UpdateApi
from Apis.thingInspections.queryThingInspectionRules import InspectionRule
import random


class UpdateThingInspectionFeedback(UpdateApi):
    NORMAL = "NORMAL"
    ABNORMAL = "ABNORMAL"

    def __init__(self, _id=None, things_ids=None, user=None):
        super(UpdateThingInspectionFeedback, self).__init__("updateThingInspectionFeedback", user)
        self.id = _id
        self.things_ids = things_ids

    def feedback(self, rule: InspectionRule, is_complete=True, thing_repair_ids=None, _id=None):
        if self.id and not _id:
            _id = self.id
        if not thing_repair_ids:
            thing_repair_ids = []
        results = self._return_results(rule, is_complete)
        var = {
            "thingRepairs": [{"id": i} for i in thing_repair_ids],
            "results": results
        }
        self.update(_id, variables=var)
        return self.result

    def _return_results(self, rule: InspectionRule, is_complete):
        results = []
        flag = self.NORMAL
        if is_complete:
            thing_ids = self.things_ids
        else:
            thing_ids = self.things_ids[1:]
        for thing in thing_ids:
            records = []
            for sub_item in rule.sub_items:
                record = {
                    "subItemId": sub_item.id,
                    "result": flag,
                    "images": [{"id": 1}, {"id": 2}]
                }
                if sub_item.category == sub_item.NUMBER:
                    value = self._from_flag_return_value(flag, sub_item.criteria, sub_item.boundary)
                    # 现在全部是由前端进行判断
                    # record.pop("result")
                    record.update(value=10)
                records.append(record)
                flag = self.ABNORMAL
            result = {
                "thingId": thing,
                "remarks": "记录设备id为%s的设备" % thing,
                "records": records
            }
            results.append(result)
        return results

    def _from_flag_return_value(self, flag, criteria, boundary):
        a = boundary.get("a")
        b = boundary.get("b")
        if criteria == "GT_LOWER_LT_UPPER":
            if flag == self.NORMAL:
                return random.choice([a + 1, b - 1])
            else:
                return random.choice([a, b])
        elif criteria == "GE_LOWER_LT_UPPER":
            if flag == self.NORMAL:
                return random.choice([a, b - 1])
            else:
                return random.choice([a - 1, b])
        elif criteria == "GE_LOWER_LE_UPPER":
            if flag == self.NORMAL:
                return random.choice([a, b])
            else:
                return random.choice([a - 1, b + 1])
        elif criteria == "GT_LOWER_LE_UPPER":
            if flag == self.NORMAL:
                return random.choice([a + 1, b])
            else:
                return random.choice([a, b + 1])
        elif criteria == "GE":
            if flag == self.NORMAL:
                return random.choice([a + 1, a])
            else:
                return random.choice([a - 1, a - 2])
        elif criteria == "GT":
            if flag == self.NORMAL:
                return random.choice([a + 1, a + 2])
            else:
                return random.choice([a - 1, a])
        elif criteria == "LE":
            if flag == self.NORMAL:
                return random.choice([a, a - 1])
            else:
                return random.choice([a + 1, a + 2])
        elif criteria == "LT":
            if flag == self.NORMAL:
                return random.choice([a - 2, a - 1])
            else:
                return random.choice([a, a + 1])
        elif criteria == "NOTEQUAL":
            if flag == self.NORMAL:
                return random.choice([a - 1, a + 1])
            else:
                return random.choice([a])
        elif criteria == "EQUAL":
            if flag == self.NORMAL:
                return random.choice([a])
            else:
                return random.choice([a - 1, a + 1])
