from support.base_test.base_api.SpecialApi import CreateApi
from support import create_timestamp


class CreateThingInspection(CreateApi):

    def __init__(self, user=None):
        super(CreateThingInspection, self).__init__("createThingInspection", user)

    def create_inspection(self, rule_id, operation_id, thing_id_list: list, period_type="SINGLE",
                          start=create_timestamp(), end=None, frequency=None):
        var = {
            "rule": {"id": rule_id},
            "things": [{"id": i} for i in thing_id_list],
            "operator": {"id": operation_id},
            "period": {
                "type": period_type,
                "startAt": start,
                "endAt": end,
                "frequency": frequency
            }
        }

        return self.create(var)
