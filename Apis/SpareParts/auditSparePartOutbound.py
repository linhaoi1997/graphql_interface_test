from support import BaseApi


class AuditSparePartOutbound(BaseApi):
    def __init__(self, user=None, _id=None):
        super(AuditSparePartOutbound, self).__init__("auditSparePartOutbound", user)
        self.id = _id

    def audit(self, details, action, _id=None, **kwargs):
        if self.id and not _id:
            _id = self.id
        if not details and kwargs.get("spare_part_list"):
            num = kwargs.pop("spare_part_num")
            details = [{"sparePart": {"id": i}, "actual_number": num} for i in kwargs.pop("spare_part_list")]
        variables = {
            "input": {
                "id": _id,
                "action": action,
                "details": details
            }
        }
        return self.run(variables)

    def audit_pass(self, details=None, _id=None, **kwargs):
        return self.audit(details, "APPROVE", _id, **kwargs)

    def audit_reject(self, details=None, _id=None, **kwargs):
        return self.audit(details, "REJECT", _id, **kwargs)
