from support.base_test.ResourceLoader import ResourceLoader
from support.base_test.generate_param.GenerateParam import GraphqlInterface
import pytest
import os

s = ResourceLoader()
simple_user = s.simple_user
pro_dir = os.path.dirname(__file__)
xml_path = pro_dir + "/output/report/xml/"
all_param = {
    "list_len": 2,
    "num": 1,
    "is_random": True,
    "no_none": True,
}


def create(_create_list, num):
    def _create(_query_name, _num):
        while _num > 0:
            interface = GraphqlInterface(_query_name)
            variable = next(interface.generate_no_optional_params(**all_param))
            result = simple_user.send_request(_query_name, variable)
            if not result.find_result("$..errors")[0]:
                print(" %s success %s \n" % (_query_name, _num))
            else:
                print(" %s fail %s \n" % (_query_name, _num))
                break
            _num -= 1

    for query_name in _create_list:
        _create(query_name, num)


if __name__ == '__main__':
    pytest.main(['-v', "-s", "interface", '--alluredir', xml_path])
    create_list = ["createThing", "createSparePart", "createSparePartReceipt", "create"]
