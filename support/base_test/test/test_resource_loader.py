from support.base_test.ResourceLoader import ResourceLoader, IdMap, UserLoader
from support.base_test.GenerateParam import GraphqlInterface
from beeprint import pp

if __name__ == '__main__':
    s = ResourceLoader()
    pp(s.interface.interfaces)
    test = GraphqlInterface("createThingInspectionRule")
    test_identity = {
        "list_len": 2,
        "num": 1,
        "is_random": True,
        "rule_id": 2,
        # "no_optional": True,
        # "no_none": True
    }
    variables = test.generate_params(**test_identity)

    pp(s.create("createThingInspectionRule", variables))
    pp(s.id)