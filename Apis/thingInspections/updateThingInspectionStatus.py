from support.base_test.base_api.BaseApi import BaseApi


class UpdateThingInspectionStatus(BaseApi):

    def __init__(self, user=None, _id=None):
        super(UpdateThingInspectionStatus, self).__init__("updateThingInspectionStatus", user)
        self.id = _id

    def audit(self, action, _id=None):
        if not _id and self.id:
            _id = self.id
        var = {
            "input": {
                "id": _id,
                "action": action
            }
        }
        return self.run(var)

    def audit_START_INSPECTION(self, _id=None):
        return self.audit("START_INSPECTION", _id)

    def audit_COMMIT(self, _id=None):
        return self.audit("COMMIT", _id)

    def audit_APPROVE_FEEDBACK(self, _id=None):
        return self.audit("APPROVE_FEEDBACK", _id)

    def audit_REJECT_FEEDBACK(self, _id=None):
        return self.audit("REJECT_FEEDBACK", _id)
