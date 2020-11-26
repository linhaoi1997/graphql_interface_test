from support.base_test.base_api.SpecialApi import UpdateApi


class UpdateThingMaintenanceFeedback(UpdateApi):
    def __init__(self, _id=None, user=None):
        super(UpdateThingMaintenanceFeedback, self).__init__("updateThingMaintenanceFeedback", user)
        self.id = _id

    def feedback(self):
        var = {
            "images": [{"id": 1}, {"id": 2}],
            "remarks": "接口测试",
        }
        return self.update(variables=var)
