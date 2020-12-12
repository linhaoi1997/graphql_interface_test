from Apis.thingRepairs.createThingRepair import CreateThingRepair
from Apis.Things.things import Things, Thing
from Apis.thingRepairs.auditThingRepair import AuditThingRepair
from Apis.thingRepairs.updateThingRepairFeedback import UpdateThingRepairFeedback
from Apis.thingRepairs.updateThingRepair import UpdateThingRepair
from Apis.thingRepairs.thingRepairs import QueryThingRepairs, QueryThingRepair
from Apis.Things.updateThing import UpdateThing
from Apis.Things.thingOverView import ThingOverView
from support import resource, record
import random
import allure


class ThingRepairFlow(object):

    def __init__(self):
        # 初始化人员
        self.report_user = resource.get_user("report_user")
        self.audit_user = resource.get_user("audit_user")
        self.feed_back_user = resource.get_user("feed_back_user")
        self.other_user = resource.get_user("other_user")
        self.see_all_user = resource.get_user("see_all_user")
        self.standby_user = resource.get_user("standby_user")

        # 权限测试，三个人员的overview
        self.report_user_overview = ThingOverView(self.report_user)
        self.feed_back_user_overview = ThingOverView(self.feed_back_user)
        self.audit_user_overview = ThingOverView(self.audit_user)
        self.other_user_overview = ThingOverView(self.other_user)
        self.standby_user_overview = ThingOverView(self.standby_user)
        self.see_all_user_overview = ThingOverView(self.see_all_user)
        self.old_report_user_count = self.report_user_overview.thingRepairToFinishedCount
        self.old_feedback_user_count = self.feed_back_user_overview.thingRepairToFinishedCount
        self.old_audit_user_count = self.audit_user_overview.thingRepairToFinishedCount
        self.old_other_user_count = self.other_user_overview.thingRepairToFinishedCount
        self.old_see_all_user_count = self.see_all_user_overview.thingRepairToFinishedCount
        self.old_standby_user_count = self.standby_user_overview.thingRepairToFinishedCount

        # 创建表单
        self.create_repair = CreateThingRepair(self.report_user)
        with allure.step("选择设备并更新thing的设备维护人"):
            thing_id = random.choice(Things(self.report_user).query_and_return_ids())
            record(thing_id, "thing_id")
            worker_ids = [self.report_user.id, self.feed_back_user.id, self.other_user.id]
            UpdateThing(thing_id).update_repair_contacts(
                worker_ids=worker_ids)
            for i in worker_ids:
                ids = Thing().query_and_return_contact_ids(thing_id)
                assert i in ids
            for i in Thing().query_and_return_contact_ids(thing_id):
                assert i in worker_ids
        self.create_repair.create_repair(thing_id)
        self.id = self.create_repair.id

        # 审核指派人员
        self.audit = AuditThingRepair(self.id, self.audit_user)
        self.feedback_action = AuditThingRepair(self.id, self.report_user)

        # 反馈
        self.feedback = UpdateThingRepairFeedback(self.id, self.feed_back_user)
        self.other_feedback = UpdateThingRepairFeedback(self.id, self.other_user)

        # 重写工单
        self.update_repair = UpdateThingRepair(self.id, self.report_user)

        # 查询工单
        self.report_user_see = QueryThingRepairs(self.report_user)
        self.feed_back_user_see = QueryThingRepairs(self.feed_back_user)
        self.audit_user_see = QueryThingRepairs(self.audit_user)
        self.other_user_see = QueryThingRepairs(self.other_user)
        self.see_all_user_see = QueryThingRepairs(self.see_all_user)
        self.standby_user_see = QueryThingRepairs(self.standby_user)

        self.report_user_see_one = QueryThingRepair(self.report_user)
        self.feed_back_user_see_one = QueryThingRepair(self.feed_back_user)
        self.audit_user_see_one = QueryThingRepair(self.audit_user)
        self.other_user_see_one = QueryThingRepair(self.other_user)
