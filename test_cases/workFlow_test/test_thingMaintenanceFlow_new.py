from Apis.WorkFlow.ThingMaintenanceFlow import ThingMaintenanceFlow
from support import BaseTestCase, run
import allure


class TestMaintenanceFlow(BaseTestCase):

    def maintenance(self):
        with allure.step("创建保养单"):
            flow = ThingMaintenanceFlow()
            self.assertCorrect(flow.create_maintenance.result)
            assert flow.query.query_and_find_status() == "PENDING"
        with allure.step("反馈保养单"):
            flow.feedback_action.audit_START_MAINTENANCE()
            assert flow.query.query_and_find_status() == "MAINTAINING"
            flow.feedback.feedback()
            assert flow.query.query_and_find_status() == "UNDERREVIEW"
        return flow

    @allure.title("创建、反馈、审核通过")
    def test_1(self):
        flow = self.maintenance()
        with allure.step("审核通过"):
            flow.audit.audit_APPROVE_FEEDBACK()
            assert flow.query.query_and_find_status() == "FINISHED"

    @allure.title("创建、反馈、拒绝、反馈、通过")
    def test_2(self):
        def assert_maintenance_in_user():
            assert flow.id in flow.report_user_query.query_and_return_ids()
            assert flow.id in flow.audit_user_query.query_and_return_ids()
            assert flow.id in flow.feedback_user_query.query_and_return_ids()
            assert flow.id in flow.see_all_user_query.query_and_return_ids()
            assert flow.id not in flow.other_user_query.query_and_return_ids()

        with allure.step("创建保养单"):
            flow = self.maintenance()
            assert_maintenance_in_user()
        with allure.step("审核拒绝"):
            flow.audit.audit_REJECT_FEEDBACK()
            assert flow.query.query_and_find_status() == "MAINTAINING"
        with allure.step("反馈保养单"):
            flow.feedback.feedback()
            assert flow.query.query_and_find_status() == "UNDERREVIEW"
        with allure.step("审核通过"):
            flow.audit.audit_APPROVE_FEEDBACK()
            assert flow.query.query_and_find_status() == "FINISHED"

    @allure.title("权限测试，查看看到的工单数")
    def test_3(self):
        def assert_thing_maintenance_count(count):
            assert flow.report_user_overview.thingMaintenanceToFinishedCount == flow.old_report_user_count + \
                   count \
                   and flow.feed_back_user_overview.thingMaintenanceToFinishedCount == \
                   flow.old_feedback_user_count + count \
                   and flow.audit_user_overview.thingMaintenanceToFinishedCount == flow.old_audit_user_count + \
                   count \
                   and flow.see_all_user_overview.thingMaintenanceToFinishedCount == flow.old_see_all_user_count + \
                   count

        with allure.step("创建工单"):
            flow = self.maintenance()
            assert_thing_maintenance_count(1)
            assert flow.other_user_overview.thingMaintenanceToFinishedCount == flow.old_other_user_count
        with allure.step("反馈保养单"):
            flow.feedback.feedback()
            assert_thing_maintenance_count(1)
            assert flow.other_user_overview.thingMaintenanceToFinishedCount == flow.old_other_user_count
        with allure.step("审核通过"):
            flow.audit.audit_APPROVE_FEEDBACK()
            assert_thing_maintenance_count(0)
            assert flow.other_user_overview.thingMaintenanceToFinishedCount == flow.old_other_user_count


if __name__ == '__main__':
    run(__file__)
