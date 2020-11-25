from support.base_test.GraphqlClient import GraphqlClient
from copy import deepcopy


class Status(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.allowed_actions = kwargs.get("actions")

    def allow(self, action):
        if action.name in self.allowed_actions:
            return True
        else:
            return False

    def get(self, action):
        return self.allowed_actions[action.name]


class Action(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.args = kwargs.get("args")
        self.user = kwargs.get("user")


class WorkFlowUser(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.client = GraphqlClient(kwargs.get("login"))

    def __call__(self, action, *args, **kwargs):
        run = getattr(self, action)
        return run(*args, **kwargs)

    def update_information(self, information_dict):
        for key, value in information_dict.items():
            setattr(self, key, value)


class Operator(object):

    def __init__(self):
        self.users = {}
        self.statuses = {}
        self.actions = {}
        self.all_actions = []
        self.start_status = None
        self.create_user = None
        self.error_record = {}
        self.last_user = None

    def init(self, flow_information):
        for user in flow_information["users"]:
            self.users[user.get("name")] = user
        for status in flow_information["all_status"]:
            self.statuses[status.get("name")] = Status(**status)
        all_actions = []
        for action in flow_information["all_actions"]:
            action_name = action.get("name")
            all_actions.append(action_name)
            self.actions[action_name] = Action(**action)
        self.all_actions = all_actions
        objects = flow_information["object"]
        self.start_status = objects.get("start_status")
        self.create_user = objects.get("create_user")

    def __getattr__(self, item):
        if "user" in item:
            return self.users.get(item)

    def generator(self, flow: list = []):
        action_list = self.all_actions
        if not flow:
            status = self.statuses.get(self.start_status)
            flow.append(status.name)
        else:
            status = self.statuses.get(flow[-1])
        for action_name in action_list:
            action = self.actions.get(action_name)
            if status.allow(action) and self._judge(flow, action, status):
                flow.append(action.name)
                flow.append(status.get(action))
                yield from self.generator(flow)
            elif self._judge(flow, action, status):
                if self._filter_error(status, action):
                    flow.append(action.name)
                    flow.append("error")
                    yield deepcopy(flow)
                else:
                    yield deepcopy(flow)
                    continue
            else:
                break
            flow.pop()
            flow.pop()

    def generate_test_case(self):
        test_cases = []
        for test_case in self.generator():
            test_cases.append("-->".join(test_case))
        return sorted(set(test_cases))

    @staticmethod
    def _judge(flow, action, status):
        flag = 0
        status = status.name
        action = action.name
        for i in range(len(flow) - 1):
            if flow[i] == action and flow[i + 1] == status:
                flag += 1
        # print(flag)
        return flag < 2

    def _filter_error(self, status, action):
        flag = True
        if isinstance(self.error_record.get(status.name), list):
            if action.name in self.error_record[status.name]:
                flag = False
            else:
                self.error_record[status.name].append(action.name)
        else:
            self.error_record[status.name] = [action.name]
        # print(self.error_record)
        return flag

    def init_user(self, user):
        for user_name, user_information in self.users.items():
            setattr(self, user_name, user(**user_information))

    def do(self, user_name, action, *args, **kwargs):
        print("user %s do %s" % (user_name, action))
        user = getattr(self, user_name)
        self.last_user = user
        result = user(action, *args, **kwargs)
        if result:
            for u in self.users.values():
                temp_user = getattr(self, u.get("name"))
                temp_user.update_information(result)

    def execute(self, test_case):
        print("execute test_case : %s" % test_case)
        steps = test_case.split("-->")
        start_status = steps.pop(0)
        self.do(self.create_user, "start")
        self.do(self.create_user, "assert_me", start_status)
        while steps:
            action = steps.pop(0)
            status = steps.pop(0)
            user = self.actions.get(action).user
            self.do(user, action)
            self.do(user, "assert_me", status)


if __name__ == '__main__':
    test = {
        "all_status": [
            {"name": "REJECT", "actions": {"re_submit": "DISPATCHING"}},
            {"name": "DISPATCHING",
             "actions": {"audit_pass": "REPAIRING", "audit_reject": "REJECT", "audit_stop": "STOP"}},
            {"name": "REPAIRING", "actions": {"feed": "FEEDBACK", "audit_stop": "STOP"}},
            {"name": "FEEDBACK",
             "actions": {"audit_feed_pass": "FINISHED", "audit_feed_reject": "REPAIRING",
                         "audit_stop": "STOP"}},
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
            {"name": "simple_user", "login": None}
        ],
        "object": {
            "query": "create_thing_repair",
            "query_return": "thing_repair_id",
            "start_status": "DISPATCHING"
        }

    }

    a = Operator()
    a.init(test)
    print(a.users)

    a.simple_user = WorkFlowUser(**test["users"][0])
    print(a.simple_user)
    # print(a.statuses)
    # print(a.actions)
    # b = []
    # for j in a.generate_test_case():
    #     b.append(j)
    #     # print(a.error_record)
    # print(len(b))
    # for k in b:
    #     print(k)
