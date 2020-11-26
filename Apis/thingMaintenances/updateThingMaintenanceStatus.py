from support.base_test.base_api.SpecialApi import UpdateApi


class UpdateThingMaintenanceStatus(UpdateApi):

    def __init__(self, _id=None, user=None):
        super(UpdateThingMaintenanceStatus, self).__init__("updateThingMaintenanceStatus", user)
        self.id = _id

    def audit(self, action):
        var = {
            "id": self.id,
            "action": action
        }
        return self.update(variables=var)

    def audit_START_MAINTENANCE(self):
        self.audit("START_MAINTENANCE")

    def audit_APPROVE_FEEDBACK(self):
        self.audit("APPROVE_FEEDBACK")

    def audit_REJECT_FEEDBACK(self):
        self.audit("REJECT_FEEDBACK")
