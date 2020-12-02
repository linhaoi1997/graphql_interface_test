from Apis.WorkFlow.ThingRepairFlow import ThingRepairFlow
from support import BaseTestCase, run
import allure


class TestWorkFlowTestCases(BaseTestCase):

    @allure.title("发起维修单、审核指派人员、反馈、通过")
    def test_1(self):
        with allure.step("发起维修单"):
            flow = ThingRepairFlow()
            with allure.step("权限校验，目前只有发起人和审核人员可以看见工单"):
                assert flow.id in flow.report_user_see.query_and_return_ids()
                assert flow.id in flow.audit_user_see.query_and_return_ids()
                assert flow.id not in flow.feed_back_user_see.query_and_return_ids()
                assert flow.id not in flow.other_user_see.query_and_return_ids()
            with allure.step("校验工单状态为派工中"):
                assert flow.report_user_see_one.return_thing_repair_status(flow.id) == "DISPATCHING"
        with allure.step("第一次审核"):
            flow.audit.audit_APPROVE_REPAIR([flow.feed_back_user.id, flow.other_user.id])
            with allure.step("权限校验，目前维修人员也能看见工单了"):
                assert flow.id in flow.feed_back_user_see.query_and_return_ids()
                assert flow.id in flow.other_user_see.query_and_return_ids()
            with allure.step("校验工单状态为维修中"):
                assert flow.report_user_see_one.return_thing_repair_status(flow.id) == "REPAIRING"
        with allure.step("反馈"):
            flow.feedback.update()
            with allure.step("校验工单状态为反馈中"):
                assert flow.report_user_see_one.return_thing_repair_status(flow.id) == "FEEDBACK"
        with allure.step("不通过"):
            with allure.step("只有发起人可以审核，其他人审核报错"):
                flow.audit.audit_REJECT_REPAIR()
                self.assertError(flow.audit.result)
            with allure.step("发起人审核可以通过"):
                flow.feedback_action.audit_REJECT_FEEDBACK()
                with allure.step("校验工单状态为维修中"):
                    assert flow.report_user_see_one.return_thing_repair_status(
                        flow.id) == flow.report_user_see_one.REPAIRING
        with allure.step("反馈"):
            flow.feedback.update()
            with allure.step("校验工单状态为反馈中"):
                assert flow.report_user_see_one.return_thing_repair_status(flow.id) == "FEEDBACK"
        with allure.step("通过"):
            flow.feedback_action.audit_APPROVE_FEEDBACK([flow.feed_back_user.id])
            with allure.step("lin 看到的工单状态应该为终止,另一个人看到的工单状态应该为完成"):
                assert flow.feed_back_user_see_one.return_thing_repair_status(flow.id) == "FINISHED"
                assert flow.other_user_see_one.return_thing_repair_status(flow.id) == "STOP"

    @allure.title("发起维修单、拒绝")
    def test_2(self):
        with allure.step("发起维修单"):
            flow = ThingRepairFlow()
            with allure.step("校验工单状态为派工中"):
                assert flow.report_user_see_one.return_thing_repair_status(flow.id) == "DISPATCHING"
        with allure.step("第一次审核拒绝"):
            flow.audit.audit_REJECT_REPAIR()
            assert flow.report_user_see_one.return_thing_repair_status(flow.id) == flow.report_user_see_one.REJECT
        with allure.step("重新编辑提交"):
            flow.update_repair.update_repair()
            assert flow.report_user_see_one.return_thing_repair_status(flow.id) == flow.report_user_see_one.DISPATCHING

    @allure.title("发起维修单、终止")
    def test_3(self):
        with allure.step("发起维修单"):
            flow = ThingRepairFlow()
            with allure.step("校验工单状态为派工中"):
                assert flow.report_user_see_one.return_thing_repair_status(flow.id) == "DISPATCHING"
        with allure.step("第一次审核终止"):
            flow.audit.audit_STOP()
            assert flow.report_user_see_one.return_thing_repair_status(flow.id) == flow.report_user_see_one.STOP


if __name__ == '__main__':
    run(__file__)
