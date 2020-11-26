from support.base_test.base_api.SpecialApi import CreateApi


class CreateThingRepair(CreateApi):

    def __init__(self, user=None):
        super(CreateThingRepair, self).__init__("createThingRepair", user)

    def create_repair(self, thing_id):
        var = {"thing": {"id": thing_id}}
        return self.create(var)
