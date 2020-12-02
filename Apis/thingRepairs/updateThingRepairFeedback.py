from support.base_test.base_api.SpecialApi import UpdateApi


class UpdateThingRepairFeedback(UpdateApi):
    def __init__(self, _id=None, user=None):
        super(UpdateThingRepairFeedback, self).__init__("updateThingRepairFeedback", user)
        self.id = _id
