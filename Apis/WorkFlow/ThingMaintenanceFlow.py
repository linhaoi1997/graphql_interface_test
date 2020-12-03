from support import resource
from Apis.thingMaintenances.createThingMaintenance import CreateThingMaintenance
from Apis.thingMaintenances.queryThingMaintenanceRules import QueryThingMaintenanceRules
from Apis.thingMaintenances.updateThingMaintenanceStatus import UpdateThingMaintenanceStatus
from Apis.thingMaintenances.updateThingMaintenanceFeedback import UpdateThingMaintenanceFeedback
from Apis.thingMaintenances.queryThingMaintenance import QueryMaintenance, QueryMaintenances
from Apis.Things.things import Things
from Apis.Things.thingOverView import ThingOverView
import allure


class ThingMaintenanceFlow(object):

    def __init__(self):
        # 初始化人员
        self.report_user = resource.get_user("report_user")
        self.audit_user = resource.get_user("audit_user")
        self.feed_back_user = resource.get_user("feed_back_user")
        self.other_user = resource.get_user("other_user")
        self.see_all_user = resource.get_user("see_all_user")

        __id = QueryMaintenances(self.report_user).query_and_return_first_id()
        # 权限测试，四个人员的overview
        self.report_user_overview = ThingOverView(self.report_user)
        self.feed_back_user_overview = ThingOverView(self.feed_back_user)
        self.audit_user_overview = ThingOverView(self.audit_user)
        self.other_user_overview = ThingOverView(self.other_user)
        self.see_all_user_overview = ThingOverView(self.see_all_user)
        self.old_report_user_count = self.report_user_overview.thingMaintenanceToFinishedCount
        self.old_feedback_user_count = self.feed_back_user_overview.thingMaintenanceToFinishedCount
        self.old_audit_user_count = self.audit_user_overview.thingMaintenanceToFinishedCount
        self.old_other_user_count = self.other_user_overview.thingMaintenanceToFinishedCount
        self.old_see_all_user_count = self.see_all_user_overview.thingMaintenanceToFinishedCount

        # 创建表单
        self.create_maintenance = CreateThingMaintenance(self.report_user)
        self.rule = QueryThingMaintenanceRules(self.report_user).return_random_rule()
        self.things_ids = Things().query_and_return_ids(limit=1)
        self.create_maintenance.create_maintenance(self.rule.id, self.feed_back_user.id, self.things_ids)
        self.id = QueryMaintenances(self.report_user).query_and_return_first_id()
        with allure.step("确认成功创建保养单"):
            assert __id != self.id

        # 审核/更新/反馈
        self.audit = UpdateThingMaintenanceStatus(self.id, self.audit_user)
        self.feedback = UpdateThingMaintenanceFeedback(self.id, self.feed_back_user)
        self.feedback_action = UpdateThingMaintenanceStatus(self.id, self.feed_back_user)
        # 查询
        self.query = QueryMaintenance(self.id, self.report_user)

        # 四个查询
        self.report_user_query = QueryMaintenances(self.report_user)
        self.feedback_user_query = QueryMaintenances(self.feed_back_user)
        self.audit_user_query = QueryMaintenances(self.audit_user)
        self.other_user_query = QueryMaintenances(self.other_user)
        self.see_all_user_query = QueryMaintenances(self.see_all_user)
