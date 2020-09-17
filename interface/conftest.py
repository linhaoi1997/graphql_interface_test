import pytest
from support import init_data, ResourceLoader, GraphqlInterface, logger
from support.base_test.FormStruct import recover_form_struct, test_form_struct
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


@pytest.fixture(scope="session", autouse=True)
def init():
    # init_data()
    # test_form_struct()
    pass


s = ResourceLoader()
id_map = {
    "Thing": [1, 2, 3],
    "SparePart": [1, 2, 3],
    "attachment": [1, 2, 3, 4],
    "image": [1, 2, 3],
    "faultImage": [1, 2, 3, 4, 5],
    "ThingMaintenanceRule": [1],
    "ThingInspectionRule": [1],
    "ThingRepair": [1],
    "ThingMaintenance": [1],
    "operator": [1],
    "worker": [1],
    "maintainer": [1],
    "parent": [2, 1],
    "permission": [1, 2, 3],
    "role": [1, 2, 3],
    "department": [1, 2, 3],
}
s.import_id(id_map)
all_param = {
    "list_len": 3,
    "num": 1,
    "is_random": True,
    "no_none": True,
}


@pytest.fixture(scope="session", autouse=True)
def resource():
    return s


# @pytest.fixture(scope="session")
# def generate_param():
#     return GraphqlInterface()


@pytest.fixture(scope="function")
def create_id():
    def _create_id(create_name, num, name, return_type="id"):
        create_interface = GraphqlInterface(create_name)
        _ids = []
        variable = {}
        _id_map = {}
        while num > 0:
            variable = next(create_interface.generate("generate_all_params", **all_param))
            _id_map = s.create(create_name, variable)
            logger.debug(_id_map)
            _ids.append(_id_map[name][0])
            num -= 1
        if return_type == "id":
            return _ids
        elif return_type == "variable":
            return _ids[0], variable
        elif return_type == "result":
            return _ids[0], _id_map

    return _create_id


def _create_var(query_name):
    v = GraphqlInterface(query_name)
    identity = {
        "list_len": 1,
        "num": 1,
        "is_random": True,
        "rule_id": 2,
        # "no_optional": True,
        # "no_none": True
    }
    return query_name, v.generate_params()


if __name__ == "__main__":
    test_form_struct(False)
