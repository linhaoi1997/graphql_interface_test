from support import BaseApi


class CreateSparePartReceipt(BaseApi):
    def __init__(self, user=None):
        super(CreateSparePartReceipt, self).__init__("createSparePartReceipt", user)

    def create_receipt(self, **kwargs):
        self.variables.get("input").update({"shelf": "测试仓库", "factory": "测试工厂", "operator": {"id": self.user.id}})
        details = []
        if kwargs.get("spare_part_list"):
            spare_part_list = kwargs.pop("spare_part_list")
            num = kwargs.pop("spare_part_num")
            details = [{"sparePart": {"id": spare_part}, "number": num} for spare_part in spare_part_list]
        if details:
            self.change_value("input.details", details)
        return self.run()
