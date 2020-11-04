from support.base_test.newSchema import Param, Schema, Input, eam_schema
from support.base_test.Fake import fake
import time
import random


class GenerateInput(object):

    @classmethod
    def _generate(cls, schema: Schema, _input: Input, **identity):
        result = {}
        for param in _input.params:
            result.update(getattr(GenerateParam(), param.type)(schema, param, **identity))

        return result

    @classmethod
    def generate(cls, schema: Schema, _input: Input, **identity):
        return {_input.name: cls._generate(schema, _input, **identity)}

    @classmethod
    def generate_root(cls, schema: Schema, _input: Input, **identity):
        return cls._generate(schema, _input, **identity)


class GenerateParam(object):
    def __getattr__(self, item: str):
        all_base_type = ("Int", "Float", "String", "ID", "Boolean", "Upload", "JSONString", "Timestamp")
        if item in all_base_type:
            return getattr(self, "generate_" + item.lower())
        else:
            return self.generate_enum_or_input

    @staticmethod
    def generate_string(schema: Schema, param: Param, **identity):
        return StringParam(schema, param).generate(**identity)

    @staticmethod
    def generate_id(schema: Schema, param: Param, **identity):
        return IDParam(schema, param).generate(**identity)

    @staticmethod
    def generate_int(schema: Schema, param: Param, **identity):
        return IntParam(schema, param).generate(**identity)

    @staticmethod
    def generate_float(schema: Schema, param: Param, **identity):
        return FloatParam(schema, param).generate(**identity)

    @staticmethod
    def generate_upload(schema: Schema, param: Param, **identity):
        return UploadParam(schema, param).generate(**identity)

    @staticmethod
    def generate_boolean(schema: Schema, param: Param, **identity):
        return BooleanParam(schema, param).generate(**identity)

    @staticmethod
    def generate_jsonstring(schema: Schema, param: Param, **identity):
        return JSONStringParam(schema, param).generate(**identity)

    @staticmethod
    def generate_timestamp(schema: Schema, param: Param, **identity):
        return TimestampParam(schema, param).generate(**identity)

    @staticmethod
    def generate_enum(schema: Schema, param: Param, **identity):
        return EnumParam(schema, param).generate(**identity)

    @staticmethod
    def generate_input(schema: Schema, param: Param, **identity):
        return InputParam(schema, param).generate(**identity)

    @staticmethod
    def generate_enum_or_input(schema: Schema, param: Param, **identity):
        if getattr(schema.enum, param.type):
            return EnumParam(schema, param).generate(**identity)
        else:
            return InputParam(schema, param).generate(**identity)


class BaseParam(object):

    def __init__(self, schema: Schema, param: Param):
        self.schema = schema
        self.param = param

    def generate(self, **identity):
        if identity.get("no_optional") and not self.param.is_must:
            if identity.get("no_none"):
                return {}
            else:
                return {self.param.name: None}
        elif self.param.is_list:
            _len = identity.get("list_len", 1)
            return {self.param.name: [self._generate(**identity) for i in range(_len)]}
        else:
            return {self.param.name: self._generate(**identity)}

    def _generate(self, **identity):
        pass


class StringParam(BaseParam):

    def _generate(self, **identity):
        return fake.create_string(self, **identity)


class IntParam(BaseParam):
    def _generate(self, **identity):
        return identity.get("int", 1)


class FloatParam(BaseParam):
    def _generate(self, **identity):
        return identity.get("float", 1.01)


class IDParam(BaseParam):
    def _generate(self, **identity):
        return None


class BooleanParam(BaseParam):
    def _generate(self, **identity):
        return identity.get("boolean", True)


class UploadParam(BaseParam):
    def _generate(self, **identity):
        return None


class JSONStringParam(BaseParam):
    def _generate(self, **identity):
        return {}


class TimestampParam(BaseParam):
    def _generate(self, **identity):
        return int(time.time() * 1000) + identity.get("delay", 0) * 60 * 1000


class EnumParam(BaseParam):
    def _generate(self, **identity):
        return identity.get(self.param.type, random.choice(getattr(self.schema.enum, self.param.type).value_list))


class InputParam(BaseParam):
    def _generate(self, **identity):
        _input2 = getattr(self.schema, self.param.type)
        if _input2 is None:
            raise Exception("no input named %s" % self.param.type)
        return GenerateInput.generate(self.schema, _input2, **identity)[self.param.type]


class GraphqlInterface(object):

    def __init__(self, query_name):
        self.query_name = query_name

    def generate_params(self, **identity):
        return GenerateInput.generate_root(eam_schema, getattr(eam_schema, self.query_name), **identity)

    def generate_all_params(self, **identity):
        yield self.generate_params(**identity)

    def generate_no_optional_params(self, **identity):
        identity.update({"no_optional": True})
        yield self.generate_params(**identity)


if __name__ == '__main__':
    test = GraphqlInterface("ExportThingInput")

    print(test.generate_params(list_len=3))

    test = GenerateInput.generate_root(eam_schema, eam_schema.things)
    print(test)
