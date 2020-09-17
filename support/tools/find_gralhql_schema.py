import os
from support.caps.read_yaml import get_file_path
import re
from beeprint import pp

file_path = get_file_path("schema_graphql")
platform_file_path = get_file_path("platform_graphql")
schema_path = get_file_path("schema")


# 查找npm生成的标准graphql接口
def find_schema(schema_type="queries", name="accountExist", is_platform=False, has_typename=True):
    if not is_platform:
        file_name = os.path.join(file_path, schema_type, name) + ".gql"
    else:
        file_name = os.path.join(platform_file_path, schema_type, name) + ".gql"
    with open(file_name) as f:
        query_str: str = f.read()
    if has_typename:
        query_str = query_str.replace("}", " __typename }", query_str.count("}") - 1)

    return query_str


def find_input(schema_type="queries", name="accountExist"):
    return find(schema_type, name, "input")


def find(schema_type="queries", name="accountExist", find_type="input"):
    file_name = os.path.join(file_path, schema_type, name) + ".gql"
    with open(file_name) as f:
        query_str: str = f.read()
    _query = re.search("\$%s: (\w+)!" % find_type, query_str)
    if _query:
        input_name = _query.group(1)
    else:
        input_name = name
    return input_name


def find_return_type(query_name):
    with open(schema_path) as f:
        query_str: list = f.readlines()
    for i in query_str:
        if i.strip().startswith(query_name):
            return i.split(":")[-1].strip().rstrip("!")


def find_test_file(file_name="26f175eaa2634bedabc4694c688bd522.jpeg"):
    dir_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file_name = os.path.join(dir_path, "support/test_file", file_name)
    with open(file_name, mode="rb") as f:
        msg = f.read()
    return msg


if __name__ == "__main__":
    query = find_schema(schema_type="mutations", name="createSparePartOutbound")
    # query = find_test_file()
    print(query)
