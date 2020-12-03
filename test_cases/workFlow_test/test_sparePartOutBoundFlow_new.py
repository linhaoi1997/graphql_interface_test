from Apis.WorkFlow.SparepartOutboundFlow import SparePartOutboundFlow
from Apis.SpareParts.querySparePartStocks import QuerySparePartStocks
from support import BaseTestCase, run
import allure


class TestSparePartOutboundFlow(BaseTestCase):

    @allure.title("申请备件->通过->完成")
    def test_1(self):
        with allure.step("创建出库单"):
            flow = SparePartOutboundFlow()
        with allure.step("审核通过,库存减少,工单状态改变为通过"):
            spare_part_num = 100
            flow.audit.audit_pass(spare_part_list=flow.spare_part_list, spare_part_num=spare_part_num)
            now_stocks = QuerySparePartStocks(flow.report_user).query_and_return_stocks(
                spare_part_list=flow.spare_part_list)
            for _id, numbers in flow.stocks.items():
                assert now_stocks[_id] == numbers - spare_part_num
            status = flow.query.query_and_return_status()
            assert status == "APPROVED"

    @allure.title("申请备件->拒绝->再次编辑->通过")
    def test_2(self):
        with allure.step("创建出库单"):
            flow = SparePartOutboundFlow()
        with allure.step("审核拒绝,库存不变，状态变为拒绝中"):
            flow.audit.audit_reject()
            now_stocks = QuerySparePartStocks(flow.report_user).query_and_return_stocks(
                spare_part_list=flow.spare_part_list)
            for _id, numbers in flow.stocks.items():
                assert now_stocks[_id] == numbers
            status = flow.query.query_and_return_status()
            assert status == "REJECTED"
        with allure.step("再次编辑"):
            flow.feed_back.update_part(variables=flow.create.variables.get("input"))
            status = flow.query.query_and_return_status()
            assert status == "PENDING"
        with allure.step("审核通过,库存减少,工单状态改变为通过"):
            spare_part_num = 100
            flow.audit.audit_pass(spare_part_list=flow.spare_part_list, spare_part_num=spare_part_num)
            now_stocks = QuerySparePartStocks(flow.report_user).query_and_return_stocks(
                spare_part_list=flow.spare_part_list)
            for _id, numbers in flow.stocks.items():
                assert now_stocks[_id] == numbers - spare_part_num
            status = flow.query.query_and_return_status()
            assert status == "APPROVED"

    @allure.title("申请备件->通过但是库存没有这么多值导致失败")
    def test_3(self):
        with allure.step("创建出库单"):
            flow = SparePartOutboundFlow()
        with allure.step("审核通过,库存减少,工单状态改变为通过"):
            spare_part_num = 1000000
            # 很大的的值
            flow.audit.audit_pass(spare_part_list=flow.spare_part_list, spare_part_num=spare_part_num)
            now_stocks = QuerySparePartStocks(flow.report_user).query_and_return_stocks(
                spare_part_list=flow.spare_part_list)
            for _id, numbers in flow.stocks.items():
                assert now_stocks[_id] == numbers
            status = flow.query.query_and_return_status()
            assert status == "PENDING"
            # 有一个值符合但是依然不能过
            flow.audit.change_value("input.details[0].actual_number", 100)
            flow.audit.audit_pass(spare_part_list=flow.spare_part_list, spare_part_num=spare_part_num)
            now_stocks = QuerySparePartStocks(flow.report_user).query_and_return_stocks(
                spare_part_list=flow.spare_part_list)
            for _id, numbers in flow.stocks.items():
                assert now_stocks[_id] == numbers
            status = flow.query.query_and_return_status()
            assert status == "PENDING"

    @allure.title("备件各流程，移动端角标和概览的数量变化")
    def test_4(self):
        def assert_spare_outbound_count(count):
            assert flow.report_user_overview.sparePartOutboundToFinishedCount == flow.old_report_user_count + \
                   count and flow.feed_back_user_overview.sparePartOutboundToFinishedCount == \
                   flow.old_feedback_user_count + \
                   count and flow.audit_user_overview.sparePartOutboundToFinishedCount == flow.old_audit_user_count + \
                   count

        with allure.step("创建出库单"):
            flow = SparePartOutboundFlow()
            with allure.step("执行人、审核人、发起人的未完成备件数量+1,其他人员不变"):
                assert_spare_outbound_count(1)
                assert flow.other_user_overview.sparePartOutboundToFinishedCount == flow.old_other_user_count
        with allure.step("拒绝出库单"):
            flow.audit.audit_reject()
            with allure.step("执行人、审核人、发起人的未完成备件数量不变,其他人员不变"):
                assert_spare_outbound_count(1)
                assert flow.other_user_overview.sparePartOutboundToFinishedCount == flow.old_other_user_count
        with allure.step("再次编辑入库单"):
            flow.feed_back.update_part(variables=flow.create.variables.get("input"))
            with allure.step("执行人、审核人、发起人的未完成备件数量不变,其他人员不变"):
                assert_spare_outbound_count(1)
                assert flow.other_user_overview.sparePartOutboundToFinishedCount == flow.old_other_user_count
        with allure.step("审核通过"):
            spare_part_num = 100
            flow.audit.audit_pass(spare_part_list=flow.spare_part_list, spare_part_num=spare_part_num)
            with allure.step("执行人、审核人、发起人的未完成备件数量-1,其他人员不变"):
                assert_spare_outbound_count(0)
                assert flow.other_user_overview.sparePartOutboundToFinishedCount == flow.old_other_user_count


if __name__ == '__main__':
    run(__file__)
