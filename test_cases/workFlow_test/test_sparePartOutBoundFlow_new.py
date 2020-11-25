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


if __name__ == '__main__':
    run(__file__)
