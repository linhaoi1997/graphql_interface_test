from support.base_test.generate_param.newSchema import base_schema, Schema
from support.base_test.generate_param.GenerateParam import GraphqlInterface
from support.base_test.ResourceLoader import resource


class BaseApi(object):
    def __init__(self, api_name, user=resource.simple_user, schema: Schema = base_schema):
        self.schema = schema
        self.api_name = api_name
        self.user = user
        self.interface_generator = GraphqlInterface(api_name, schema)
        self.variables = self.interface_generator.generate_params()
        self.result = None

    def run(self):
        self.result = self.user.send_request(self.api_name, self.variables).result

    @property
    def variables(self):
        return self.variables

    @variables.setter
    def variables(self, variables):
        self.variables = variables
