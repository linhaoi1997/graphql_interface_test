from support import GraphqlClient, create_timestamp, AssertMethod, logger, run, config
import allure
import pytest

THING = {"id": 1}
WORKER = {"id": 137}


class ThingRepairUser(AssertMethod):

    def __init__(self, login=None):
        self.user = GraphqlClient(login)
        self.feed_number = 1
        self.result = None

        # 多加一个创建工单以每次测试使用

    def create_thing_repair(self):
        query_name = "createThingRepair"
        variables = {
            "input": {
                "thing": THING,
                "faultDesc": "接口测试流程故障",
                "reportedAt": create_timestamp(),
                "reportDepartment": "接口测试部门",
                "worker": WORKER,
            }
        }
        thing_repair_id = self.user(query_name, variables).find_result("$..id")[0]
        logger.debug("thing_repair_id =" + str(thing_repair_id))
        return thing_repair_id

    # 五个动作：1: 审核（通过/拒绝）参数应该均为维修单的ID,返回值待定

    def audit(self, _id, action):
        query_name = "updateThingRepairStatus"
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
        result = self.audit(_id, "APPROVE_REPAIR")
        self.assertJsonResponseEqual("$..status", result, "REPAIRING")

    # 拒绝申请
    def audit_reject(self, _id):
        result = self.audit(_id, "REJECT_REPAIR")
        self.assertJsonResponseEqual("$..status", result, "REJECT")

    # 反馈通过
    def audit_feed_pass(self, _id):
        result = self.audit(_id, "APPROVE_FEEDBACK")
        self.assertJsonResponseEqual("$..status", result, "FINISHED")
        return result

    # 反馈拒绝
    def audit_feed_reject(self, _id):
        result = self.audit(_id, "REJECT_FEEDBACK")
        self.assertJsonResponseEqual("$..status", result, "REPAIRING")

    # 终止
    def audit_stop(self, _id):
        result = self.audit(_id, "STOP")
        self.assertJsonResponseEqual("$..status", result, "STOP")

    # 2: 派工中审核拒绝后重新编辑（提交）,输入应为id
    def re_submit(self, _id):
        query_name = "updateThingRepair"
        variables = {
            "input": {
                "id": _id,
                "thing": THING,
                "faultDesc": "接口测试流程故障",
                "reportedAt": create_timestamp(),
                "reportDepartment": "接口测试部门",
                "worker": WORKER,
            }
        }
        result = self.user(query_name, variables).result
        self.result = result
        self.assertJsonResponseEqual("$..status", result, "DISPATCHING")

    def feed(self, _id):
        query_name = "updateThingRepairFeedback"
        variables = {
            "input": {
                "id": _id,
                "result": "接口测试结果" + str(self.feed_number),
                "finishedAt": create_timestamp(),
                "sparePartCosts": 100,
                "materialCosts": 100,
                "laborCosts": 100,
                "otherCosts": 100
            }
        }
        self.feed_number += 1
        result = self.user(query_name, variables).result
        self.result = result
        self.assertJsonResponseEqual("$..status", result, "FEEDBACK")


@allure.epic("workflow")
@allure.feature("ThingRepairWorkFlow")
class TestThingRepairWorkFlow(AssertMethod):
    feed_back_user = ThingRepairUser(config.get_account("feed_back_user"))
    audit_user = ThingRepairUser(config.get_account("audit_user"))

    @allure.story("派工中->维修中->反馈中->维修完成")
    def test_1(self):
        thing_repair_id = self.audit_user.create_thing_repair()
        # 第一次审核通过
        self.audit_user.audit_pass(thing_repair_id)
        # 反馈
        self.feed_back_user.feed(thing_repair_id)
        # 反馈审核通过
        self.audit_user.audit_feed_pass(thing_repair_id)

    @allure.story("派工中->维修中->反馈中->反馈拒绝->再次反馈->反馈通过")
    def test_2(self):
        thing_repair_id = self.audit_user.create_thing_repair()
        # 第一次审核通过
        self.audit_user.audit_pass(thing_repair_id)
        # 反馈提交
        self.feed_back_user.feed(thing_repair_id)
        # 反馈审核拒绝
        self.audit_user.audit_feed_reject(thing_repair_id)
        # 再次反馈提交
        self.feed_back_user.feed(thing_repair_id)
        # 反馈审核通过
        result = self.audit_user.audit_feed_pass(thing_repair_id)
        self.assertJsonCountEqual("$..resultHistory[*]", result, 2)

    @allure.story("派工中->维修中->审核拒绝->重新提交->审核通过->维修中")
    def test_3(self):
        thing_repair_id = self.audit_user.create_thing_repair()
        # 第一次审核拒绝
        self.audit_user.audit_reject(thing_repair_id)
        #  再次提交
        self.audit_user.re_submit(thing_repair_id)
        #  第一次审核通过
        self.audit_user.audit_pass(thing_repair_id)

    @allure.story("派工中->终止")
    def test_4(self):
        thing_repair_id = self.audit_user.create_thing_repair()
        # 终止流程
        self.audit_user.audit_stop(thing_repair_id)

    @allure.story("派工中-> 维修中->终止")
    def test_5(self):
        thing_repair_id = self.audit_user.create_thing_repair()
        # 第一次审核通过
        self.audit_user.audit_pass(thing_repair_id)
        # 终止流程
        self.audit_user.audit_stop(thing_repair_id)

    @allure.story("派工中-> 维修中-> 反馈中->终止")
    def test_6(self):
        thing_repair_id = self.audit_user.create_thing_repair()
        # 第一次审核通过
        self.audit_user.audit_pass(thing_repair_id)
        # 反馈
        self.feed_back_user.feed(thing_repair_id)
        # 终止流程
        self.audit_user.audit_stop(thing_repair_id)

    def _call_action(self, user, action, _id):
        call_str = "self.{user}.{action}({_id})".format(user=user, action=action, _id=_id)
        try:
            exec(call_str)
            # 如果通过了这个步骤说明不对
            pytest.fail("本来不应该通过这个步骤，这不正常！！！")
        except AssertionError as e:
            logger.debug(e)
        # 如果未通过校验（校验部分是核实返回的status是否是预期的），那么检查下它是不是有报错也是有必要的
        self.assertError(getattr(self, user).result)

    # 预期错误的用例
    test_data = ["re_submit", "feed", "audit_feed_pass", "audit_feed_reject"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("派工中不允许的操作")
    def test_7(self, action):
        thing_repair_id = self.audit_user.create_thing_repair()
        self._call_action("audit_user", action, thing_repair_id)

    # 预期错误的用例
    test_data = ["feed", "audit_pass", "audit_reject", "audit_feed_pass", "audit_feed_reject",
                 ]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("拒绝中不允许的操作")
    def test_8(self, action):
        thing_repair_id = self.audit_user.create_thing_repair()
        # 审核拒绝
        self.audit_user.audit_reject(thing_repair_id)
        self._call_action("audit_user", action, thing_repair_id)

    # 预期错误的用例
    test_data = ["re_submit", "audit_pass", "audit_reject", "audit_feed_pass", "audit_feed_reject"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("维修中不允许的操作")
    def test_9(self, action):
        thing_repair_id = self.audit_user.create_thing_repair()
        # 审核通过->维修中
        self.audit_user.audit_pass(thing_repair_id)
        self._call_action("audit_user", action, thing_repair_id)

    # 预期错误的用例
    test_data = ["re_submit", "feed", "audit_pass", "audit_reject"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("反馈中不允许的操作")
    def test_10(self, action):
        thing_repair_id = self.audit_user.create_thing_repair()
        # 审核通过->维修中
        self.audit_user.audit_pass(thing_repair_id)
        # 提交反馈 ->反馈中
        self.feed_back_user.feed(thing_repair_id)
        self._call_action("audit_user", action, thing_repair_id)

    # 预期错误的用例
    test_data = ["re_submit", "feed", "audit_pass", "audit_reject", "audit_feed_pass", "audit_feed_reject",
                 "audit_stop"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("维修完成不允许的操作")
    def test_11(self, action):
        thing_repair_id = self.audit_user.create_thing_repair()
        # 审核通过->维修中
        self.audit_user.audit_pass(thing_repair_id)
        # 提交反馈 ->反馈中
        self.feed_back_user.feed(thing_repair_id)
        # 反馈审核通过->维修完成
        self.audit_user.audit_feed_pass(thing_repair_id)
        self._call_action("audit_user", action, thing_repair_id)

    # 预期错误的用例
    test_data = ["re_submit", "feed", "audit_pass", "audit_reject", "audit_feed_pass", "audit_feed_reject",
                 "audit_stop"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("终止不允许的操作")
    def test_12(self, action):
        thing_repair_id = self.audit_user.create_thing_repair()
        # 终止->终止
        self.audit_user.audit_stop(thing_repair_id)
        self._call_action("audit_user", action, thing_repair_id)

    all_action = ["re_submit", "feed", "audit_pass", "audit_reject", "audit_feed_pass", "audit_feed_reject",
                  "audit_stop"]


if __name__ == "__main__":
    run(__file__)
