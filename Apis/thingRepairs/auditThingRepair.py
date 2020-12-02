from support.base_test.base_api.SpecialApi import UpdateApi


class AuditThingRepair(UpdateApi):

    def __init__(self, _id=None, user=None):
        super(AuditThingRepair, self).__init__("auditThingRepair", user)
        self.id = _id

    def audit(self, action, workers_ids=None):
        if workers_ids is None:
            workers_ids = []
        var = {
            "action": action,
            "workers": [{"id": i} for i in workers_ids]
        }
        return self.update(variables=var)

    def audit_APPROVE_REPAIR(self, workers):
        self.audit("APPROVE_REPAIR", workers)

    def audit_REJECT_REPAIR(self):
        self.audit("REJECT_REPAIR")

    def audit_APPROVE_FEEDBACK(self, workers):
        self.audit("APPROVE_FEEDBACK", workers)

    def audit_REJECT_FEEDBACK(self):
        self.audit("REJECT_FEEDBACK")

    def audit_STOP(self):
        self.audit("STOP")
