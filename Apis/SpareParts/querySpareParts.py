from support.base_test.base_api.SpecialApi import QueryManyApi
import random


class QuerySpareParts(QueryManyApi):

    def __init__(self, user=None):
        super(QuerySpareParts, self).__init__("spareParts", user)

    def return_random_spare_part(self):
        return random.choice(self.query_and_return_ids())
