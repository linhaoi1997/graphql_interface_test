import os
from support.caps.read_yaml import config
import re

file_path = config.get_file_path("schema_graphql")
platform_file_path = config.get_file_path("platform_graphql")
schema_path = config.get_file_path("schema")


class Query(object):

    def __init__(self, query_file_path=config.get_file_path("schema_graphql")):
        self.query_path = os.path.join(query_file_path, "queries")
        self.mutation_path = os.path.join(query_file_path, "mutations")
        self._query = os.listdir(self.query_path)
        self._mutation = os.listdir(self.mutation_path)
        self.all_query = {}

    def get_query(self, name="accountExist", has_typename=True):
        if name + ".gql" in self._query:
            file_name = os.path.join(self.query_path, name) + ".gql"
        elif name + ".gql" in self._mutation:
            file_name = os.path.join(self.mutation_path, name) + ".gql"
        else:
            raise Exception("没有对应接口，看下是否需要更新schema")
        with open(file_name) as f:
            query_str: str = f.read()
        if has_typename:
            query_str = query_str.replace("}", " __typename }", query_str.count("}") - 1)
        return query_str

    def find_input(self, name):
        query = self.get_query(name)
        _query = re.search("\$input: (\w+)!", query)
        if _query:
            input_name = _query.group(1)
        else:
            input_name = name
        return input_name

    def __getattr__(self, item):
        if item not in self.all_query.keys():
            self.all_query[item] = self.get_query(item)
        return self.all_query[item]


graphql_query = Query()
platform_query = Query(platform_file_path)


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
    print(graphql_query.login)
    print(graphql_query.find_input("login"))
