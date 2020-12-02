from support.base_test.generate_param.newSchema import Param, Schema, Input, base_schema
from support.base_test.generate_param.Fake import fake
from support.base_test.ResourceLoader import resource
import time
import random
import json


class GenerateInput(object):

    @classmethod
    def _format(cls, name: str):
        if name.endswith("s"):
            name = name[:-1]
        return name

    @classmethod
    def _generate(cls, schema: Schema, _input: Input, **identity):
        result = {}
        identity.update({"input_name": cls._format(_input.name)})
        for param in _input.params:
            identity.update({"param_name": cls._format(param.name)})
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
        all_base_type = ("Int", "Float", "String", "ID", "IDInput", "Boolean", "Upload", "JSONString", "Timestamp")
        if item in all_base_type:
            return getattr(self, "generate_" + item.lower())
        elif "JSONString" in item:
            return self.generate_jsonstring
        else:
            return self.generate_enum_or_input

    @staticmethod
    def generate_string(schema: Schema, param: Param, **identity):
        return StringParam(schema, param).generate(**identity)

    @staticmethod
    def generate_id(schema: Schema, param: Param, **identity):
        return IDParam(schema, param).generate(**identity)

    @staticmethod
    def generate_idinput(schema: Schema, param: Param, **identity):
        return IDInputParam(schema, param).generate(**identity)

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
        try:
            return resource.get_id(identity.get("param_name"))
        except KeyError:
            try:
                return resource.get_id(identity.get("input_name"))
            except KeyError:
                print("未找到 %s 下 %s 参数的 id，请手动填入" % (identity.get("input_name"), identity.get("param_name")))
                return None


class IDInputParam(BaseParam):
    def _generate(self, **identity):
        try:
            return {"id": resource.get_id(identity.get("param_name"))}
        except KeyError:
            try:
                return {"id": resource.get_id(identity.get("input_name"))}
            except KeyError:
                print("未找到 %s 下 %s 参数的 id，请手动填入" % (identity.get("input_name"), identity.get("param_name")))
                return {"id": None}


class BooleanParam(BaseParam):
    def _generate(self, **identity):
        return identity.get("boolean", True)


class UploadParam(BaseParam):
    def _generate(self, **identity):
        return None


class JSONStringParam(BaseParam):
    def _generate(self, **identity):
        _input2 = getattr(self.schema, self.param.type)
        if _input2 is None:
            raise Exception("no input named %s" % self.param.type)
        var = [GenerateInput.generate(self.schema, _input2, **identity)[self.param.type]]
        if var[0] == {}:
            var = []
        result = json.dumps(var)
        return result


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

    def __init__(self, query_name, schema: Schema = base_schema):
        self.query_name = query_name
        self.schema = schema

    def generate_params(self, **identity):
        return GenerateInput.generate_root(self.schema, getattr(self.schema, self.query_name), **identity)

    def generate_all_params(self, **identity):
        yield self.generate_params(**identity)

    def generate_no_optional_params(self, **identity):
        identity.update({"no_optional": True})
        yield self.generate_params(**identity)

    def generate(self, method, **kwargs):
        return getattr(self, method)(**kwargs)


if __name__ == '__main__':
    test = GraphqlInterface("exportSparePartReceipts")

    print(test.generate_params(list_len=3, no_none=True))

    test = GenerateInput.generate_root(base_schema, base_schema.things)
    print(test)
