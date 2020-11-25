from support.base_test.base_api.SpecialApi import UpdateApi


class UpdateSparePartOutbound(UpdateApi):

    def __init__(self, user, _id):
        super(UpdateSparePartOutbound, self).__init__("updateSparePartOutbound", user)
        self.id = _id
