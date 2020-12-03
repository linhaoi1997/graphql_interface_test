from support import resource
from Apis.thingInspections.createThingInspection import CreateThingInspection
from Apis.thingInspections.updateThingInspectionStatus import UpdateThingInspectionStatus
from Apis.thingInspections.queryThingInspectionRules import QueryThingInspectionRules
from Apis.thingInspections.updateThingInspectionFeedback import UpdateThingInspectionFeedback
from Apis.thingInspections.queryInspection import QueryInspection, QueryInspections
from Apis.thingRepairs.createThingRepair import CreateThingRepairs
from Apis.Things.thingOverView import ThingOverView
from Apis.Things.things import Things


class TestInspectionFlow(object):

    def __init__(self):
        # 初始化人员
        self.report_user = resource.get_user("report_user")
        self.audit_user = resource.get_user("audit_user")
        self.feed_back_user = resource.get_user("feed_back_user")
        self.other_user = resource.get_user("other_user")
        self.see_all_user = resource.get_user("see_all_user")

        # 权限测试，四个人员的overview
        self.report_user_overview = ThingOverView(self.report_user)
        self.feed_back_user_overview = ThingOverView(self.feed_back_user)
        self.audit_user_overview = ThingOverView(self.audit_user)
        self.other_user_overview = ThingOverView(self.other_user)
        self.see_all_user_overview = ThingOverView(self.see_all_user)
        self.old_report_user_count = self.report_user_overview.thingInspectionToFinishedCount
        self.old_feedback_user_count = self.feed_back_user_overview.thingInspectionToFinishedCount
        self.old_audit_user_count = self.audit_user_overview.thingInspectionToFinishedCount
        self.old_other_user_count = self.other_user_overview.thingInspectionToFinishedCount
        self.old_see_all_user_count = self.see_all_user_overview.thingInspectionToFinishedCount

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

        # 所有人员的查询
        self.report_user_query = QueryInspections(self.report_user)
        self.feedback_user_query = QueryInspections(self.feed_back_user)
        self.audit_user_query = QueryInspections(self.audit_user)
        self.other_user_query = QueryInspections(self.other_user)
        self.see_all_user_query = QueryInspections(self.see_all_user)
