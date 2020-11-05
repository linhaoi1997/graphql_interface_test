from support.base_test.generate_param.GenerateParam import GraphqlInterface
from support.base_test.ResourceLoader import ResourceLoader

s = ResourceLoader()
if __name__ == "__main__":
    id_map = {
        "Thing": [1, 2, 3, 4],
        "SparePart": [1, 2, 3, 5, 8],
        "attachment": [1, 2, 3, 4],
        "image": [1, 2, 3, 4, 5],
        "thinginspectionrule": ["asdasdasd", "1212121ijsda"]
    }
    s.import_id(id_map)
    test = GraphqlInterface("updateThing")
    test_identity = {
        "list_len": 1,
        "num": 1,
        "is_random": True,
        # "rule_id": 2,
        # "no_optional": True,
        "no_none": True
    }
    variables = test.generate_all_params(**test_identity)

    for i in variables:
        print(i)

