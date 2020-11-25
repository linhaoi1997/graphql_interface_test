from support import BaseApi


class CreateSparePartOutbound(BaseApi):
    def __init__(self, user=None):
        super(CreateSparePartOutbound, self).__init__("createSparePartOutbound", user)

    def create_outbound(self, operator_id: int, reason="", **kwargs):
        self.variables.get("input").update({"shelf": "测试仓库", "factory": "测试工厂", "reason": reason})
        self.change_value("input.operator", {"id": operator_id})
        details = []
        if kwargs.get("spare_part_list"):
            spare_part_list = kwargs.pop("spare_part_list")
            num = kwargs.pop("spare_part_num")
            details = [{"sparePart": {"id": spare_part}, "number": num} for spare_part in spare_part_list]
        if details:
            self.change_value("input.details", details)
        self.variables.get("input").update(**kwargs)
        self.run()
        self.id = self.find_first_deep_item("id")
        return self.result

    def create_outbound_by_thingRepair(self, operator_id, repair_id, **kwargs):
        self.change_value("input.thingRepair", {"id": repair_id})
        self.pop_value("input.thingMaintenance")
        self.pop_value("input.thingInspection")
        return self.create_outbound(operator_id, reason="设备维修", **kwargs)

    def create_outbound_by_thingMaintenance(self, operator_id, maintenance_id, **kwargs):
        self.change_value("input.thingMaintenance", {"id": maintenance_id})
        self.pop_value("input.thingRepair")
        self.pop_value("input.thingInspection")
        return self.create_outbound(operator_id, reason="设备保养", **kwargs)

    def create_outbound_by_thingInspection(self, operator_id, inspection_id, **kwargs):
        self.change_value("input.thingMaintenance", {"id": inspection_id})
        self.pop_value("input.thingMaintenance")
        self.pop_value("input.thingRepair")
        return self.create_outbound(operator_id, reason="设备巡检", **kwargs)

    def create_outbound_by_other(self, operator_id, **kwargs):
        self.pop_value("input.thingMaintenance")
        self.pop_value("input.thingInspection")
        self.pop_value("input.thingRepair")
        return self.create_outbound(operator_id, reason="其它", **kwargs)
