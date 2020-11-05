from support import GraphqlClient, create_timestamp, AssertMethod, logger, run, config
import allure
import pytest

RULE = {"id": 1}
THING = {"id": 1}
MAINTAINER = {"id": 25}


class ThingMaintenanceUser(AssertMethod):

    def __init__(self, login=None):
        self.user = GraphqlClient(login)
        self.feed_number = 1
        self.result = None

        # 多加一个创建工单以每次测试使用

    def create_thing_maintenance(self, delay=0):
        query_name = "createThingMaintenance"
        variables = {
            "input": {
                "rule": RULE,
                "maintainer": MAINTAINER,
                "thing": THING,
                "period": {
                    "type": "SINGLE",
                    "startAt": create_timestamp(delay)
                }
            }
        }
        thing_maintenance_id = self.user(query_name, variables).find_result("$..id")[0]
        logger.debug("thing_maintenance_id =" + str(thing_maintenance_id))
        return thing_maintenance_id

    # 3个动作：1: 审核（通过/拒绝）参数应该均为维修单的ID,返回值待定

    def audit(self, _id, action):
        query_name = "updateThingMaintenanceStatus"
        variables = {
            "input": {
                "id": _id,
                "action": action
            }
        }
        result = self.user(query_name, variables).result
        self.result = result
        return result

    # 反馈通过
    def audit_feed_pass(self, _id):
        result = self.audit(_id, "APPROVE_FEEDBACK")
        self.assertJsonResponseEqual("$..status", result, "FINISHED")
        return result

    # 反馈拒绝
    def audit_feed_reject(self, _id):
        result = self.audit(_id, "REJECT_FEEDBACK")
        self.assertJsonResponseEqual("$..status", result, "MAINTAINING")

    # 2: 待巡检时可以编辑,输入应为id
    def update(self, _id, delay=0):
        query_name = "updateThingMaintenance"
        variables = {
            "input": {
                "id": _id,
                "rule": RULE,
                "maintainer": MAINTAINER,
                "thing": THING,
                "period": {
                    "type": "SINGLE",
                    "startAt": create_timestamp(delay)
                }
            }
        }
        result = self.user(query_name, variables).result
        self.result = result
        self.assertJsonResponseEqual("$..status", result, "PENDING")

    def feed(self, _id):
        query_name = "updateThingMaintenanceFeedback"
        variables = {
            "input": {
                "id": _id,
                "result": "接口测试执行结果",
                "remarks": "接口测试备注",
                "endAt": create_timestamp()
            }
        }
        self.feed_number += 1
        result = self.user(query_name, variables).result
        self.result = result
        self.assertJsonResponseEqual("$..status", result, "UNDERREVIEW")


@allure.epic("workflow")
@allure.feature("ThingMaintenanceWorkFlow")
class TestThingMaintenanceWorkFlow(AssertMethod):
    feed_back_user = ThingMaintenanceUser(config.get_account("feed_back_user"))
    audit_user = ThingMaintenanceUser(config.get_account("audit_user"))

    @allure.story("待保养--编辑->待保养")
    def test_1_0(self):
        thing_maintenance_id = self.audit_user.create_thing_maintenance(delay=10)
        # 更新保养单
        self.audit_user.update(thing_maintenance_id, delay=10)
        # 更新保养单
        self.audit_user.update(thing_maintenance_id)

    @allure.story("保养中--反馈->审核中--审核通过->保养完成")
    def test_1(self):
        thing_maintenance_id = self.audit_user.create_thing_maintenance()
        # 反馈
        self.feed_back_user.feed(thing_maintenance_id)
        # 反馈审核通过
        self.audit_user.audit_feed_pass(thing_maintenance_id)

    @allure.story("保养中--反馈->审核中--审核拒绝->保养中--再次反馈->审核中--审核通过->保养完成")
    def test_2(self):
        thing_maintenance_id = self.audit_user.create_thing_maintenance()
        # 反馈
        self.feed_back_user.feed(thing_maintenance_id)
        # 审核拒绝
        self.audit_user.audit_feed_reject(thing_maintenance_id)
        # 再次反馈
        self.feed_back_user.feed(thing_maintenance_id)
        # 审核通过
        self.audit_user.audit_feed_pass(thing_maintenance_id)

    @allure.story("审核拒绝--再次反馈 循环5次")
    def test_3(self):
        thing_maintenance_id = self.audit_user.create_thing_maintenance()

        def circulation(n):
            for i in range(n):
                # 反馈
                self.feed_back_user.feed(thing_maintenance_id)
                # 审核拒绝
                self.audit_user.audit_feed_reject(thing_maintenance_id)

        circulation(5)
        # 再次反馈
        self.feed_back_user.feed(thing_maintenance_id)
        # 审核通过
        self.audit_user.audit_feed_pass(thing_maintenance_id)

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
    test_data = ["audit_feed_pass", "audit_feed_reject", "update"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("保养中不允许的操作")
    def test_4(self, action):
        thing_maintenance_id = self.audit_user.create_thing_maintenance()
        self._call_action("feed_back_user", action, thing_maintenance_id)

    # 预期错误的用例
    test_data = ["feed", "update"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("审核中不允许的操作")
    def test_5(self, action):
        thing_maintenance_id = self.audit_user.create_thing_maintenance()
        # 提交审核->审核中
        self.feed_back_user.feed(thing_maintenance_id)
        self._call_action("feed_back_user", action, thing_maintenance_id)

    # 预期错误的用例
    test_data = ["feed", "audit_feed_pass", "audit_feed_reject", "update"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("保养完成不允许的操作")
    def test_6(self, action):
        thing_maintenance_id = self.audit_user.create_thing_maintenance()
        # 提交审核->审核中
        self.feed_back_user.feed(thing_maintenance_id)
        # 审核通过-> 保养完成
        self.audit_user.audit_feed_pass(thing_maintenance_id)
        self._call_action("audit_user", action, thing_maintenance_id)

    # 预期错误的用例
    test_data = ["feed", "audit_feed_pass", "audit_feed_reject"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("待保养不允许的操作")
    def test_7(self, action):
        thing_maintenance_id = self.audit_user.create_thing_maintenance(delay=10)

        self._call_action("audit_user", action, thing_maintenance_id)

    # 任务执行人员不能

    all_action = ["update", "feed", "audit_feed_pass", "audit_feed_reject"]


if __name__ == "__main__":
    run(__file__)
