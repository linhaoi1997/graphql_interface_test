from support.base_test.base_api.SpecialApi import QueryManyApi


class QuerySparePartStocks(QueryManyApi):

    def __init__(self, user=None):
        super(QuerySparePartStocks, self).__init__("sparePartStocks", user)

    def query_and_return_stocks(self, shelf="测试仓库", factory="测试工厂", spare_part_list=None):
        filter_j = {
            "shelf": shelf,
            "factory": factory
        }
        self.query(_filter=filter_j)
        stocks = {}
        for i in self.result["data"][self.api_name]["data"]:
            if i["sparePart"]["id"] in spare_part_list:
                stocks[str(i["sparePart"]["id"])] = i["inventory"]
        return stocks


class QuerySparePartReceipts(QueryManyApi):

    def __init__(self, user=None):
        super(QuerySparePartReceipts, self).__init__("sparePartReceipts", user)


class QuerySparePartOutbounds(QueryManyApi):

    def __init__(self, user=None):
        super(QuerySparePartOutbounds, self).__init__("sparePartOutbounds", user)
