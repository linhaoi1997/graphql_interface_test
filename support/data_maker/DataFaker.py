from .InputSearcher import InputSearcher
from ..tools.log import logger
from ..tools.find_gralhql_schema import graphql_query
from .GraphqlClient import GraphqlClient
from .VariableMaker import VariableMaker


class DataFaker(object):

    def __init__(self, query_name, **kwargs):
        self.graphql_client = GraphqlClient()
        self.input = graphql_query.find_input(query_name)
        self.variable = VariableMaker(InputSearcher(self.input), **kwargs)
        self.query = query_name

    def fake_data(self, num):
        for i in range(num):
            result = self.graphql_client(self.query, self.variable.real_variables)
            next(self.variable)
