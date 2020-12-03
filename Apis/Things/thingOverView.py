from support.base_test.base_api.BaseApi import BaseApi


class ThingOverView(BaseApi):

    def __init__(self, user=None):
        super(ThingOverView, self).__init__("thingOverview", user)

    @property
    def thingTotalCount(self):
        self.run()
        return self.find_first_deep_item("thingTotalCount")

    @property
    def thingTotalValue(self):
        self.run()
        return self.find_first_deep_item("thingTotalValue")

    @property
    def thingRepairToFinishedCount(self):
        self.run()
        return self.find_first_deep_item("thingRepairToFinishedCount")

    @property
    def thingMaintenanceToFinishedCount(self):
        self.run()
        return self.find_first_deep_item("thingMaintenanceToFinishedCount")

    @property
    def thingInspectionToFinishedCount(self):
        self.run()
        return self.find_first_deep_item("thingInspectionToFinishedCount")

    @property
    def sparePartOutboundToFinishedCount(self):
        self.run()
        return self.find_first_deep_item("sparePartOutboundToFinishedCount")
