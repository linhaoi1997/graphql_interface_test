from Apis.WorkFlow.ThingInspectionFlow import TestInspectionFlow
from Apis.thingRepairs.thingRepairs import QueryThingRepairs

from support import BaseTestCase, run
import allure


class TestThingInspectionFlow(BaseTestCase):

    def inspection(self, is_create_repairs=False):
        with allure.step("创建巡检单"):
            flow = TestInspectionFlow()
            self.assertCorrect(flow.create_inspection.result)
            assert flow.query.query_and_find_status() == "PENDING"
        with allure.step("点击开始巡检"):
            flow.feed_back_action.audit_START_INSPECTION()
            assert flow.query.query_and_find_status() == "INPROGRESS"
        with allure.step("反馈巡检"):
            if not is_create_repairs:
                flow.feed_back.feedback(flow.rule, is_complete=False)
                flow.feed_back.feedback(flow.rule, is_complete=True)
            else:
                repairs = flow.create_repairs.create_repairs(flow.things_ids)
                flow.feed_back.feedback(flow.rule, thing_repair_ids=repairs)
                ids = QueryThingRepairs().query_and_return_ids()
                for _id in repairs:
                    assert _id not in ids
            flow.feed_back_action.audit_COMMIT()
            assert flow.query.query_and_find_status() == "UNDERREVIEW"
        return flow

    @allure.title("发起巡检单->反馈->审核通过")
    def test_1(self):
        flow = self.inspection()
        with allure.step("审核通过"):
            flow.audit.audit_APPROVE_FEEDBACK()
            assert flow.query.query_and_find_status() == "FINISHED"

    @allure.title("发起巡检单->反馈->审核拒绝")
    def test_2(self):
        flow = self.inspection()
        with allure.step("审核拒绝"):
            flow.audit.audit_REJECT_FEEDBACK()
            assert flow.query.query_and_find_status() == "INPROGRESS"
        with allure.step("反馈巡检"):
            flow.feed_back.feedback(flow.rule, is_complete=False)
            flow.feed_back.feedback(flow.rule, is_complete=True)
            flow.feed_back_action.audit_COMMIT()
            assert flow.query.query_and_find_status() == "UNDERREVIEW"
        with allure.step("审核通过"):
            flow.audit.audit_APPROVE_FEEDBACK()
            assert flow.query.query_and_find_status() == "FINISHED"

    @allure.title("根据巡检单发起维修单")
    def test_3(self):
        flow = self.inspection(is_create_repairs=True)
        with allure.step("审核通过"):
            flow.audit.audit_APPROVE_FEEDBACK()
            assert flow.query.query_and_find_status() == "FINISHED"
            ids = QueryThingRepairs().query_and_return_ids()
            for _id in flow.create_repairs.ids:
                assert _id in ids


if __name__ == '__main__':
    run(__file__)
