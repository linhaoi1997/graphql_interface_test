from support.base_test.GraphqlInterfaceGenerate import GraphqlInterface
from support.base_test.ResourceLoader import ResourceLoader
from support.base_test.SchemaReader import SchemaReader
from support.data_maker.GraphqlClient import GraphqlClient
from beeprint import pp

s = ResourceLoader()
if __name__ == "__main__":
    test = SchemaReader()
    id_map = {
        "Thing": [1, 2, 3, 4],
        "SparePart": [1, 2, 3, 5, 8],
        "attachment": [1, 2, 3, 4],
        "image": [1, 2, 3, 4, 5],
        "thinginspectionrule": ["asdasdasd", "1212121ijsda"]
    }
    s.import_id(id_map)
    # pp(test.input)
    test = GraphqlInterface("updateThing")
    # test = GraphqlInterface("createThingInspection")
    test_identity = {
        "list_len": 1,
        "num": 1,
        "is_random": True,
        # "rule_id": 2,
        # "no_optional": True,
        "no_none": True
    }
    variables = test.generate("generate_all_params", **test_identity)
    # variables = test.generate_lack_must(**test_identity)

    # pp(variables, max_depth=10)
    # variables = test.generate_lack_must(**test_identity)
    for i in variables:
        print(i)
    #
    # pp(s.create("createThingInspectionRule", variables))
