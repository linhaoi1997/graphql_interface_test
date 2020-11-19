from support import GraphqlClient, create_timestamp, AssertMethod, record, run, config
import allure
import pytest

THING = {"id": 1}
OPERATOR = {"id": 1}
THING_REPAIR = {"id": 1}


class ThingSparePartOutboundUser(AssertMethod):

    def __init__(self, login=None):
        self.user = GraphqlClient(login)
        self.feed_number = 1
        self.result = None

        # 多加一个创建工单以每次测试使用

    def create_spare_part_outbound(self):
        query_name = "createSparePartOutbound"
        variables = {
            "input": {
                "operator": OPERATOR,
                "time": create_timestamp(),
                "shelf": "测试仓库",
                "factory": "测试工厂",
                "reason": "设备维修",
                "thingRepair": THING_REPAIR,
                "details": [
                    {
                        "number": 1,
                        "reason": "LOOSEN",
                        "sparePart": {
                            "id": 2
                        }
                    },
                ],
            }
        }
        thing_repair_id = self.user(query_name, variables).find_result("$..id")[0]
        record("spare_part_outbound =" + str(thing_repair_id))
        return thing_repair_id

    # 五个动作：1: 审核（通过/拒绝）参数应该均为备件申领单的ID,返回值待定

    def audit(self, _id, action):
        query_name = "updateSparePartOutboundStatus"
        variables = {
            "input": {
                "id": _id,
                "action": action
            }
        }
        result = self.user(query_name, variables).result
        self.result = result
        return result

    # 通过申请
    def audit_pass(self, _id):
        result = self.audit(_id, "APPROVE")
        self.assertJsonResponseEqual("$..status", result, "APPROVED")

    # 拒绝申请
    def audit_reject(self, _id):
        result = self.audit(_id, "REJECT")
        self.assertJsonResponseEqual("$..status", result, "REJECTED")

    # 2: 申领审核拒绝后重新编辑（提交）,输入应为id
    def re_submit(self, _id):
        query_name = "updateSparePartOutbound"
        variables = {
            "input": {
                "id": _id,
                "operator": OPERATOR,
                "time": create_timestamp(),
                "shelf": "测试仓库",
                "factory": "测试工厂",
                "reason": "设备维修",
                "thingRepair": THING_REPAIR,
                "details": [
                    {
                        "number": 1,
                        "reason": "LOOSEN",
                        "sparePart": {
                            "id": 2
                        }
                    },
                ],
            }
        }
        result = self.user(query_name, variables).result
        self.result = result
        self.assertJsonResponseEqual("$..status", result, "PENDING")


@allure.epic("workflow")
@allure.feature("SparePartOutBoundWorkFlow")
class TestSparePartOutBoundWorkFlow(AssertMethod):
    simple_user = ThingSparePartOutboundUser(config.get_account("simple_user"))

    @allure.story("申领->待审核->审核通过->申领完成")
    def test_1(self):
        spare_part_outbound_id = self.simple_user.create_spare_part_outbound()
        # 第一次审核通过
        self.simple_user.audit_pass(spare_part_outbound_id)

    @allure.story("申领->待审核->审核拒绝->拒绝->重新编辑->审核通过->完成")
    def test_2(self):
        spare_part_outbound_id = self.simple_user.create_spare_part_outbound()
        # 第一次审核拒绝
        self.simple_user.audit_reject(spare_part_outbound_id)
        # 重新编辑提交
        self.simple_user.re_submit(spare_part_outbound_id)
        # 审核通过
        self.simple_user.audit_pass(spare_part_outbound_id)

    @allure.story("申领->待审核->审核拒绝->拒绝")
    def test_3(self):
        spare_part_outbound_id = self.simple_user.create_spare_part_outbound()
        # 第一次审核拒绝
        self.simple_user.audit_reject(spare_part_outbound_id)

    def _call_action(self, action, _id):
        call_str = "self.simple_user.{action}({_id})".format(action=action, _id=_id)
        try:
            exec(call_str)
            # 如果通过了这个步骤说明不对
            pytest.fail("本来不应该通过这个步骤，这不正常！！！")
        except AssertionError as e:
            record(e)
        # 如果未通过校验（校验部分是核实返回的status是否是预期的），那么检查下它是不是有报错也是有必要的
        self.assertError(self.simple_user.result)

    # 预期错误的用例
    test_data = ["re_submit"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("待审核中不允许的操作")
    def test_7(self, action):
        spare_part_outbound_id = self.simple_user.create_spare_part_outbound()
        self._call_action(action, spare_part_outbound_id)

    # 预期错误的用例
    test_data = ["audit_pass", "audit_reject", "re_submit"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("完成不允许的操作")
    def test_8(self, action):
        thing_repair_id = self.simple_user.create_spare_part_outbound()
        # 审核通过
        self.simple_user.audit_pass(thing_repair_id)
        self._call_action(action, thing_repair_id)

    # 预期错误的用例
    test_data = ["audit_pass", "audit_reject"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("拒绝不允许的操作")
    def test_9(self, action):
        thing_repair_id = self.simple_user.create_spare_part_outbound()
        # 审核通过
        self.simple_user.audit_pass(thing_repair_id)
        self._call_action(action, thing_repair_id)

    all_action = ["re_submit", "feed", "audit_pass", "audit_reject", "audit_feed_pass", "audit_feed_reject",
                  "audit_stop"]


if __name__ == "__main__":
    run(__file__)
