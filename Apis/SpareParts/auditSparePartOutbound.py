from support import BaseApi


class AuditSparePartOutbound(BaseApi):
    def __init__(self, user=None):
        super(AuditSparePartOutbound, self).__init__("createDepartment", user)

    def audit_pass(self, _id, details):
        variables = {
            "input": {
                "id": _id,
                "action": "APPROVE",
                "details": details
            }
        }
        return self.run()

    def audit_reject(self, _id, details):
        variables = {
            "input": {
                "id": _id,
                "action": "REJECT",
                "details": details
            }
        }
        return self.run()
