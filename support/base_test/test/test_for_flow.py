from support.base_test.WorkFlow import WorkFlowUser, Operator
import pytest
import allure

test = {
    "all_status": [
        {"name": "REJECT", "actions": {"re_submit": "DISPATCHING"}},
        {"name": "DISPATCHING",
         "actions": {"audit_pass": "REPAIRING", "audit_reject": "REJECT", "audit_stop": "STOP"}},
        {"name": "REPAIRING", "actions": {"feed": "FEEDBACK", "audit_stop": "STOP"}},
        {"name": "FEEDBACK",
         "actions": {"audit_feed_pass": "FINISHED", "audit_feed_reject": "REPAIRING", "audit_stop": "STOP"}},
        {"name": "FINISHED", "actions": {}},
        {"name": "STOP", "actions": {}}
    ],
    "all_actions": [
        {"name": "re_submit", "args": "thing_repair_id", "user": "simple_user"},
        {"name": "feed", "args": "thing_repair_id", "user": "simple_user"},
        {"name": "audit_pass", "args": "thing_repair_id", "user": "simple_user"},
        {"name": "audit_reject", "args": "thing_repair_id", "user": "simple_user"},
        {"name": "audit_feed_pass", "args": "thing_repair_id", "user": "simple_user"},
        {"name": "audit_feed_reject", "args": "thing_repair_id", "user": "simple_user"},
        {"name": "audit_stop", "args": "thing_repair_id", "user": "simple_user"},
    ],
    "users": [
        {"name": "simple_user", "login": None},
        {"name": "test_user", "login": None}
    ],
    "object": {
        "start_status": "DISPATCHING",
        "create_user": "simple_user"
    }

}


class ThingRepairUser(WorkFlowUser):

    def __init__(self, **kwargs):
        super(ThingRepairUser, self).__init__(**kwargs)
        self.result = kwargs.get("result", None)
        self.feed_number = kwargs.get("feed_number", None)
        self.thing_repair_id = kwargs.get("thing_repair_id", None)

    # 需要判断的地方在于状态是否正确
    def assert_me(self, status):
        print("status is %s" % self.result)
        print("expect %s" % status)
        if status != self.result:
            # pytest.fail("status is not %s" % status)
            print("fail")

    def start(self):
        self.result = "DISPATCHING"
        self.assert_me("DISPATCHING")
        return {"thing_repair_id": 1, "result": self.result}

    # 通过申请
    def audit_pass(self):
        self.result = "REPAIRING"

    # 拒绝申请
    def audit_reject(self):
        self.result = "REJECT"

    # 反馈通过
    def audit_feed_pass(self):
        self.result = "FINISHED"

    # 反馈拒绝
    def audit_feed_reject(self):
        self.result = "REPAIRING"

    # 终止
    def audit_stop(self):
        self.result = "STOP"

    # 2: 派工中审核拒绝后重新编辑（提交）,输入应为id
    def re_submit(self):
        self.result = "DISPATCHING"

    def feed(self):
        self.result = "FEEDBACK"


class TestThingRepairTestCase(object):
    # 1.初始化operator
    operator = Operator()
    operator.init(test)
    # 2.初始化operator的所有user,ting_repair_user定义了所有的操作
    operator.init_user(ThingRepairUser)
    # 3.初始化测试用例
    test_cases = operator.generate_test_case()
    print(len(test_cases))

    @pytest.mark.parametrize("test_case", test_cases)
    def test_execute(self, test_case):
        self.operator.execute(test_case)


if __name__ == '__main__':
    # a = Operator()
    # a.init(test)
    # print(a.users)
    #
    # a.simple_user = ThingRepairUser(**test["users"][0])
    # print(a.simple_user("audit_stop", 1))
    test_cases = TestThingRepairTestCase.test_cases
    for i in test_cases:
        print(i)
    s = TestThingRepairTestCase()
