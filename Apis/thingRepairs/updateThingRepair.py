from support.base_test.base_api.SpecialApi import UpdateApi


class UpdateThingRepair(UpdateApi):
    def __init__(self, _id=None, user=None):
        super(UpdateThingRepair, self).__init__("updateThingRepair", user)
        self.id = _id

    def update_repair(self):
        var = {
            "faultDesc": "新的描述"
        }
        self.update(variables=var)
