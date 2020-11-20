from support import BaseApi, record, pformat


class Me(BaseApi):
    def __init__(self, user=None):
        super(Me, self).__init__("me", user)

    def me(self):
        self.run()
        record(pformat(self.result), "个人信息")
        return self.result

    def return_my_id(self):
        self.run()
        record(pformat(self.result), "个人信息")
        _id = self.find_from_result("$.data.me.id")
        return _id[0]
