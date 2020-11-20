import pytest
from support import resource as s, GraphqlInterface, record, PostgresConn
from test_cases.FormStruct import recover_form_struct
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def import_id():
    eam_sleemon = PostgresConn("eam-sleemon-test")
    id_map = {
        "Thing": eam_sleemon.get_id("things"),
        "SparePart": eam_sleemon.get_id("spare_parts"),
        "attachment": eam_sleemon.get_id("files"),
        "image": eam_sleemon.get_id("files"),
        "faultImage": eam_sleemon.get_id("files"),
        "ThingMaintenanceRule": eam_sleemon.get_id("thing_maintenance_rules"),
        "ThingInspectionRule": eam_sleemon.get_id("thing_inspection_rules"),
        "ThingRepair": eam_sleemon.get_id("thing_repairs"),
        "ThingMaintenance": eam_sleemon.get_id("thing_maintenance"),
        "operator": eam_sleemon.get_id("employees"),
        "worker": eam_sleemon.get_id("employees"),
        "maintainer": eam_sleemon.get_id("employees"),
        "parent": eam_sleemon.get_id("departments"),
        "permission": eam_sleemon.get_id("permissions"),
        "role": eam_sleemon.get_id("roles"),
        "department": eam_sleemon.get_id("departments"),
    }
    s.import_id(id_map)
    record(s.id, "收集到的所有id")
    print(s.id)


import_id()


@pytest.fixture(scope="session", autouse=True)
def init():
    # init_data()
    # test_form_struct()
    pass


all_param = {
    "list_len": 3,
    "num": 1,
    "is_random": True,
    "no_none": True,
}


@pytest.fixture(scope="session", autouse=True)
def resource():
    return s


@pytest.fixture(scope="function")
def create_id():
    def _create_id(create_name, num, name, return_type="id"):
        create_interface = GraphqlInterface(create_name)
        _ids = []
        variable = {}
        _id_map = {}
        while num > 0:
            variable = next(create_interface.generate_no_optional_params(**all_param))
            _id_map = s.create(create_name, variable)
            record(_id_map)
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
    }
    return query_name, v.generate_params()


if __name__ == "__main__":
    # test_form_struct(False)
    recover_form_struct()
