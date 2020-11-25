from support.base_test.base_api.SpecialApi import QueryManyApi


class QuerySpareParts(QueryManyApi):

    def __init__(self, user):
        super(QuerySpareParts, self).__init__("spareParts", user)
