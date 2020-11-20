from support import BaseApi


class CreateSparePartOutbound(BaseApi):
    def __init__(self, user=None):
        super(CreateSparePartOutbound, self).__init__("createSparePartOutbound", user)

    def create_outbound(self, reason="", **kwargs):
        self.variables.get("input").update({"shelf": "测试仓库", "factory": "测试工厂", "reason": reason})
        self.variables.get("input").update(**kwargs)
        self.run()
        return self.result

    def create_outbound_by_thingRepair(self):
        return self.create_outbound(reason="EQUIPMENT_REPAIR")

    def create_outbound_by_thingMaintenance(self):
        return self.create_outbound(reason="EQUIPMENT_MAINTENANCE")

    def create_outbound_by_thingInspection(self):
        return self.create_outbound(reason="EQUIPMENT_INSPECTION")

    def create_outbound_by_other(self):
        return self.create_outbound(reason="OTHER")
