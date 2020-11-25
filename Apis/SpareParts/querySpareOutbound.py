from support import BaseApi


class SparePartOutbound(BaseApi):
    def __init__(self, user=None, _id=None):
        super(SparePartOutbound, self).__init__("sparePartOutbound", user)
        self.id = _id

    def query(self, _id=None):
        if not _id and self.id:
            _id = self.id
        variables = {"id": _id}
        self.run(variables)
        return self.result

    def query_certain(self, json_path, _id=None):
        self.query(_id)
        return self.find_from_result(json_path)[0]

    def query_details(self, _id=None):
        details = self.query_certain("$..details", _id)
        return details

    def query_and_return_status(self, _id=None):
        self.query(_id)
        return self.find_first_deep_item("status")
