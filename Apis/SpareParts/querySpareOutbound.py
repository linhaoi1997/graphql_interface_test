from support import BaseApi


class SparePartOutbound(BaseApi):
    def __init__(self, user=None):
        super(SparePartOutbound, self).__init__("createDepartment", user)

    def query(self, _id):
        variables = {"id": _id}
        self.run(variables)
        return self.result

    def query_certain(self, _id, json_path):
        variables = {"id": _id}
        self.run(variables)
        return self.find_from_result(json_path)[0]

    def query_details(self, _id):
        details = self.query_certain(_id, "$..details")
        return details
