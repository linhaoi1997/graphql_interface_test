from Apis.thingRepairs.thingRepairs import QueryThingRepairs
from support import run, record


class TestThingRepair(object):
    test = QueryThingRepairs()

    def test_query(self):
        record(self.test.run_and_query_id())


if __name__ == '__main__':
    run(__file__)
