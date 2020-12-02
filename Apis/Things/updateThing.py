from support.base_test.base_api.SpecialApi import UpdateApi


class UpdateThing(UpdateApi):

    def __init__(self, _id=None, user=None):
        super(UpdateThing, self).__init__("updateThing", user)
        self.id = _id

    def update_repair_contacts(self, worker_ids):
        var = {
            "repairContacts": self.return_id_input(worker_ids)
        }
        self.update_part(variables=var)
