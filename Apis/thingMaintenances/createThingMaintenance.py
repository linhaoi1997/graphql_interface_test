from support.base_test.base_api.SpecialApi import CreateApi
from support import create_timestamp


class CreateThingMaintenance(CreateApi):

    def __init__(self, user=None):
        super(CreateThingMaintenance, self).__init__("createThingMaintenance", user)

    def create_maintenance(self, rule_id, maintainer_id, thing_id_list: list, period_type="SINGLE",
                           start=create_timestamp(), end=None, frequency=None):
        var = {
            "rule": {"id": rule_id},
            "things": [{"id": i} for i in thing_id_list],
            "maintainer": {"id": maintainer_id},
            "period": {
                "type": period_type,
                "startAt": start,
                "endAt": end,
                "frequency": frequency
            }
        }
        try:
            self.create(var)
        except AssertionError:
            return self.result
