from support import resource
from Apis.thingInspections.createThingInspection import CreateThingInspection
from Apis.thingInspections.updateThingInspectionStatus import UpdateThingInspectionStatus
from Apis.thingInspections.queryThingInspectionRules import QueryThingInspectionRules
from Apis.thingInspections.updateThingInspectionFeedback import UpdateThingInspectionFeedback
from Apis.thingInspections.queryInspection import QueryInspection
from Apis.thingRepairs.createThingRepair import CreateThingRepairs
from Apis.Things.things import Things


class TestInspectionFlow(object):

    def __init__(self):
        # 初始化人员
        self.report_user = resource.get_user("report_user")
        self.audit_user = resource.get_user("audit_user")
        self.feed_back_user = resource.get_user("feed_back_user")
        # 创建表单
        self.create_inspection = CreateThingInspection(self.report_user)
        self.rule = QueryThingInspectionRules().return_random_Rule()
        self.things_ids = Things().query_and_return_ids(limit=3)
        self.create_inspection.create_inspection(self.rule.id, self.feed_back_user.id, self.things_ids)
        self.id = self.create_inspection.id

        # 审核/更新/反馈
        self.audit = UpdateThingInspectionStatus(self.audit_user, self.id)
        self.feed_back = UpdateThingInspectionFeedback(self.id, self.things_ids, self.feed_back_user)
        self.feed_back_action = UpdateThingInspectionStatus(self.feed_back_user, self.id)

        # 查询
        self.query = QueryInspection(self.report_user, self.id)
        # 可以关联维修单到保养单
        self.create_repairs = CreateThingRepairs(self.feed_back_user)
