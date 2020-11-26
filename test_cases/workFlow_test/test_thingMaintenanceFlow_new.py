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
        flow = self.maintenance()
        with allure.step("审核拒绝"):
            flow.audit.audit_REJECT_FEEDBACK()
            assert flow.query.query_and_find_status() == "MAINTAINING"
        with allure.step("反馈保养单"):
            flow.feedback.feedback()
            assert flow.query.query_and_find_status() == "UNDERREVIEW"
        with allure.step("审核通过"):
            flow.audit.audit_APPROVE_FEEDBACK()
            assert flow.query.query_and_find_status() == "FINISHED"


if __name__ == '__main__':
    run(__file__)
