from support import GraphqlClient, create_timestamp, AssertMethod, logger, run, get_account
import allure
import pytest

RULE_ID = 1
THINGS = [
    {"id": 1},
    {"id": 2}
]
OPERATOR = {
    "id": 137
    # 执行人员小何
}


class ThingInspectionUser(AssertMethod):

    def __init__(self, login=None):
        self.user = GraphqlClient(login)
        self.feed_number = 1
        self.result = None

    # 多加一个创建工单以每次测试使用
    def create_thing_inspection(self, delay=0):
        query_name = "createThingInspection"
        variables = {
            "input": {
                "rule": {"id": RULE_ID},
                "operator": OPERATOR,
                "things": THINGS,
                "period": {
                    "type": "SINGLE",
                    "startAt": create_timestamp(delay)
                }
            }
        }
        thing_inspection_id = self.user(query_name, variables).find_result("$..id")[0]
        logger.debug("thing_inspection_id =" + str(thing_inspection_id))
        return thing_inspection_id

    # 五个动作：1: 审核（通过/拒绝）参数应该均为维修单的ID,返回值待定

    def audit(self, _id, action):
        query_name = "updateThingInspectionStatus"
        variables = {
            "input": {
                "id": _id,
                "action": action
            }
        }
        result = self.user(query_name, variables).result
        return result

    # 提交反馈
    def audit_commit(self, _id):
        result = self.audit(_id, "COMMIT")
        self.result = result
        self.assertJsonResponseEqual("$..status", result, "UNDERREVIEW")

    # 反馈通过
    def audit_feed_pass(self, _id):
        result = self.audit(_id, "APPROVE_FEEDBACK")
        self.result = result
        self.assertJsonResponseEqual("$..status", result, "FINISHED")

    # 反馈拒绝
    def audit_feed_reject(self, _id):
        result = self.audit(_id, "REJECT_FEEDBACK")
        self.result = result
        self.assertJsonResponseEqual("$..status", result, "INPROGRESS")

    # 2: 待巡检时可以编辑,输入应为id
    def update(self, _id, delay=0):
        query_name = "updateThingInspection"
        variables = {
            "input": {
                "id": _id,
                "rule": {"id": RULE_ID},
                "operator": OPERATOR,
                "things": THINGS,
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
        query_name = "updateThingInspectionFeedback"
        variables = {
            "input": {
                "id": _id,
                "results":
                    [
                        {
                            "thingId": 1,
                            "remarks": "接口测试标记",
                            "records": [
                                {"subItemId": "a4e0f4fd-1b05-4d3b-ba8c-836087402692", "result": "NORMAL", "value": 5},
                                {"subItemId": "560b96e2-fcce-40ee-9602-9b5dfb750258", "result": "NORMAL"}
                            ]

                        },
                        {
                            "thingId": 2,
                            "remarks": "接口测试标记",
                            "records": [
                                {"subItemId": "a4e0f4fd-1b05-4d3b-ba8c-836087402692", "result": "ABNORMAL",
                                 "value": 11},
                                {"subItemId": "560b96e2-fcce-40ee-9602-9b5dfb750258", "result": "ABNORMAL"}
                            ]

                        }
                    ],
                "endAt": create_timestamp()
            }
        }
        self.feed_number += 1
        self.result = self.user(query_name, variables).result
        self.assertJsonResponseEqual("$..status", self.result, "INPROGRESS")


@allure.epic("workflow")
@allure.feature("ThingInspectionWorkFlow")
class TestThingInspectionWorkFlow(AssertMethod):
    feed_back_user = ThingInspectionUser(get_account("feed_back_user"))
    audit_user = ThingInspectionUser(get_account("audit_user"))

    @allure.story("待巡检--编辑->待巡检")
    def test_1_0(self):
        thing_maintenance_id = self.audit_user.create_thing_inspection(delay=10)
        # 更新保养单
        self.audit_user.update(thing_maintenance_id, delay=10)
        # 更新保养单
        self.audit_user.update(thing_maintenance_id)

    @allure.story("巡检中->反馈->审核中->审核通过->巡检完成")
    def test_1(self):
        thing_inspection_id = self.audit_user.create_thing_inspection()
        # 反馈
        self.feed_back_user.feed(thing_inspection_id)
        self.feed_back_user.audit_commit(thing_inspection_id)
        # 反馈审核通过
        self.audit_user.audit_feed_pass(thing_inspection_id)

    @allure.story("巡检中->反馈->审核中->审核拒绝->巡检中->再次反馈->审核中->审核通过->巡检完成")
    def test_2(self):
        thing_inspection_id = self.audit_user.create_thing_inspection()
        # 反馈
        self.feed_back_user.feed(thing_inspection_id)
        self.feed_back_user.audit_commit(thing_inspection_id)
        # 审核拒绝
        self.audit_user.audit_feed_reject(thing_inspection_id)
        # 再次反馈
        self.feed_back_user.feed(thing_inspection_id)
        self.feed_back_user.audit_commit(thing_inspection_id)
        # 审核通过
        self.audit_user.audit_feed_pass(thing_inspection_id)

    @allure.story("审核拒绝->再次反馈 循环5次")
    def test_3(self):
        thing_inspection_id = self.audit_user.create_thing_inspection()

        def circulation(n):
            for i in range(n):
                # 反馈
                self.feed_back_user.feed(thing_inspection_id)
                self.feed_back_user.audit_commit(thing_inspection_id)
                # 审核拒绝
                self.audit_user.audit_feed_reject(thing_inspection_id)

        circulation(5)
        # 再次反馈
        self.feed_back_user.feed(thing_inspection_id)
        self.feed_back_user.audit_commit(thing_inspection_id)
        # 审核通过
        self.audit_user.audit_feed_pass(thing_inspection_id)

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
    test_data = ["feed", "audit_feed_pass", "audit_feed_reject"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("待巡检不允许的操作")
    def test_4_0(self, action):
        thing_inspection_id = self.audit_user.create_thing_inspection(delay=10)
        self._call_action("audit_user", action, thing_inspection_id)

    @pytest.mark.parametrize("action", test_data)
    @allure.story("待巡检不允许的操作")
    def test_4_1(self, action):
        thing_inspection_id = self.audit_user.create_thing_inspection(delay=10)
        self._call_action("feed_back_user", action, thing_inspection_id)

    # 预期错误的用例
    test_data = ["update", "audit_feed_pass", "audit_feed_reject"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("巡检中不允许的操作")
    def test_5(self, action):
        thing_inspection_id = self.audit_user.create_thing_inspection()
        self._call_action("audit_user", action, thing_inspection_id)

    # 预期错误的用例
    test_data = ["update", "feed"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("审核中不允许的操作")
    def test_6(self, action):
        thing_inspection_id = self.audit_user.create_thing_inspection()
        # 反馈->审核中
        self.feed_back_user.feed(thing_inspection_id)
        self.feed_back_user.audit_commit(thing_inspection_id)
        self._call_action("audit_user", action, thing_inspection_id)

    # 预期错误的用例
    test_data = ["update", "feed", "audit_feed_pass", "audit_feed_reject"]

    @pytest.mark.parametrize("action", test_data)
    @allure.story("巡检完成不允许的操作")
    def test_7(self, action):
        thing_inspection_id = self.audit_user.create_thing_inspection()
        # 反馈->审核中
        self.feed_back_user.feed(thing_inspection_id)
        self.feed_back_user.audit_commit(thing_inspection_id)
        # 审核通过->巡检完成
        self.audit_user.audit_feed_pass(thing_inspection_id)
        self._call_action("audit_user", action, thing_inspection_id)

    all_action = ["update", "feed", "audit_feed_pass", "audit_feed_reject"]


if __name__ == "__main__":
    run(__file__)

'''
curl 'http://192.168.1.5:8200/app/eam/graphql/?updateThingInspectionRule' \
  -H 'Connection: keep-alive' \
  -H 'Pragma: no-cache' \
  -H 'Cache-Control: no-cache' \
  -H 'accept: */*' \
  -H 'Authorization: Token ByWSv5NHtAKciYA9nsTLq6NYduBQl5VU' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4229.3 Safari/537.36' \
  -H 'content-type: application/json' \
  -H 'Origin: http://192.168.1.5:8200' \
  -H 'Referer: http://192.168.1.5:8200/subapp/eam/inspection-rule/2' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Cookie: csrftoken=DtVSaIFZVinGhQR35MDwDGcXkfDsVIVS1jQYNxAkyiD9BxlIrPZ4BqwH0vXYyZpQ; sessionid=0oxq571smd0iipm84s1wbb6zf21q82ce' \
  --data-binary $'{"operationName":"updateThingInspectionRule","variables":{"input":{"id":"2","name":"测试","items":[{"id":"02d48baa-ffdc-4a2c-8ab2-225ef313e347","name":"测试1","subItems":[{"id":"a4e0f4fd-1b05-4d3b-ba8c-836087402692","name":"数值项目","standard":"测试","category":"NUMBER","criteria":"GT_LOWER_LT_UPPER","boundary":{"a":1,"b":10}}]},{"id":"99fa4c5c-aef2-41ef-9c65-44dc8cd70b55","name":"测试2","subItems":[{"id":"560b96e2-fcce-40ee-9602-9b5dfb750258","name":"普通项目","standard":"真是普通","category":"NORMAL","criteria":null,"boundary":null}]}],"addition":"[]"}},"query":"mutation updateThingInspectionRule($input: UpdateThingInspectionRuleInput\u0021) {\\n  updateThingInspectionRule(input: $input) {\\n    id\\n    code\\n    name\\n    items {\\n      id\\n      name\\n      subItems {\\n        id\\n        name\\n        standard\\n        category\\n        criteria\\n        boundary {\\n          a\\n          b\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    updatedAt\\n    addition\\n    __typename\\n  }\\n}\\n"}' \
  --compressed \
  --insecure'''
