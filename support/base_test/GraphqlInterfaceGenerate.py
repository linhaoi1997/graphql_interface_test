import random
import types
from copy import deepcopy
import json
from .Fake import MyFaker
from ..tools import create_timestamp, create_num_string
from .ResourceLoader import ResourceLoader

resource = ResourceLoader()
fake = MyFaker()


class GraphqlInterface(object):

    def __init__(self, interface_name: str, parent=None):
        info = self.get_interface_json(interface_name)
        self.input_name = info.get("name")
        self.allow_user = info.get("allow_users")
        self.params = []
        for param in info.get("params"):
            self.params.append(
                SingleParam(param.get("name"), param.get("type"), param.get("is_must"), param.get("identity", ""),
                            param.get("interface"), param.get("len"), parent, interface_name,
                            param.get("real_name"),
                            is_file=param.get("is_file")))

    @staticmethod
    def get_interface_json(interface_name):
        return getattr(resource, interface_name)

    def generate_params(self, **identity):
        variables = {}
        for param in self.params:
            variables.update(param(**identity))
        return variables

    # 可以当作全部填写完整用例
    def generate_all_params(self, **identity):
        yield self.generate_params(**identity)

    # 不填写选填项用例
    def generate_no_optional_params(self, **identity):
        identity.update({"no_optional": True})
        yield self.generate_params(**identity)
        # identity["no_none"] = False
        # yield self.generate_params(**identity)

    #  必填项不全用例
    def generate_lack(self, **identity):
        variables = {}
        for param in self.params:
            variables.update(param(**identity))
        # 取出生成器
        records = {}
        for key, value in variables.items():
            if isinstance(value, types.GeneratorType):
                records[key] = value
            elif isinstance(value, list) and isinstance(value[0], types.GeneratorType):
                records[key] = value
        identity.pop("lack_must")
        real_variables = self.generate_params(**identity)
        for key, values in records.items():
            if isinstance(values, list):
                for num, value_ in enumerate(values):
                    for value in value_:
                        temp = real_variables[key][num]
                        real_variables[key][num] = value
                        yield deepcopy(real_variables)
                        real_variables[key][num] = temp
            else:
                for value in values:
                    temp = real_variables[key]
                    real_variables[key] = value
                    yield deepcopy(real_variables)
                    real_variables[key] = temp

    def generate_lack_must(self, **identity):
        identity.update({"is_random": True, "lack_must": True, "lamb": "generate_lack_must"})
        for variables in self.generate_lack(**identity):
            yield variables
        identity.pop("lack_must")
        for param in self.params:
            if param.is_must:
                variables = self.generate_params(**identity)
                if identity.get("no_none"):
                    variables.pop(param.name)
                else:
                    variables[param.name] = None
                print("lack must of %s" % param.name)
                yield deepcopy(variables)

    # 不正常长度用例
    def generate_dan_len(self, **identity):
        identity.update({"is_random": True, "lack_must": True, "lamb": "generate_dan_len"})
        for variables in self.generate_lack(**identity):
            yield variables
        identity.pop("lack_must")
        for param in self.params:
            variables = self.generate_params(**identity)
            if param.length:
                length = param.length[1] + 1
                it = create_num_string(length, 3)
                if param.param_type == "Float" or param.param_type == "Int":
                    it = int(it)
                variables[param.name] = it
                yield variables
                length = param.length[0] - 1  # if param.length[0] > 1 else 1
                it = create_num_string(length, 3)
                if param.param_type == "Float" or param.param_type == "Int":
                    it = int(it)
                variables[param.name] = it
                yield deepcopy(variables)

    # 不正常类型用例
    def generate_dan_type(self, **identity):
        identity.update({"is_random": True, "lack_must": True, "lamb": "generate_dan_type"})
        for variables in self.generate_lack(**identity):
            yield variables
        identity.pop("lack_must")
        for param in self.params:
            variables = self.generate_params(**identity)
            print("change type of %s" % param.name)
            if param.param_type == "Float" or param.param_type == "Int":
                variables[param.name] = create_num_string(5)
            else:
                variables[param.name] = float(create_num_string(5, 3))
            yield deepcopy(variables)

    @staticmethod
    def _change_addition(variables):
        if variables.get("input"):
            if variables.get("input").get("addition") == {}:
                variables["input"]["addition"] = json.dumps([])
            elif variables.get("input").get("addition"):
                addition = [{"key": key, "value": value} for key, value in variables["input"]["addition"].items()]
                variables["input"]["addition"] = json.dumps(addition)

        return variables

    def generate(self, item, **identity):
        if "generate" in item:
            for i in getattr(self, item)(**identity):
                # print(i)
                yield self._change_addition(i)


class SingleParam(object):

    def __init__(self, name, param_type, is_must, identity, interface, field_len, parent=None, input_name=None,
                 real_name=None, is_file=False):
        self.length = field_len
        self.name = name  # 参数名称
        self.param_type = param_type  # 参数类型
        self.is_must = is_must  # 是否必填
        self.identity = identity  # 标识额外的类型以防不测（list，input）
        self.interface = interface  # 如果是ID/enum/input类型，那么使用的接口是什么
        self.parent = parent
        self.input_name = input_name
        self.real_name = real_name
        self.is_file = is_file

    def _generate(self, **identity):

        no_optional = identity.get("no_optional", False)
        # print(self.param_type,self.name)
        create_str = "_create_" + self.param_type.lower()

        create = getattr(self, create_str)
        # 如果传入参数直接用传入的
        if identity.get(self.name):
            return {self.name: identity.get(self.name)}
        # 如果没有传入参数那么生成参数
        if no_optional and not self.is_must:
            if identity.get("no_none"):
                return {}
            elif "list" in self.identity:
                variable = []
            else:
                variable = None
        elif "list" in self.identity:
            variable = list()
            list_len = identity.get("list_len", 1)
            for i in range(list_len):
                variable.append(create(**identity))
        else:
            variable = create(**identity)
        return {self.name: variable}

    def _create_id(self, **identity):
        result_id = resource.get_id(self)
        if "input" in self.name:
            return {"id": result_id}
        return result_id

    @staticmethod
    def _create_attachment(**identity):
        user = resource.simple_user
        return user.upload_file()

    def _create_string(self, **identity):
        return fake.create_string(self, **identity)

    @staticmethod
    def _create_timestamp(**identity):
        if identity.get("delay"):
            return create_timestamp() + identity.get("delay") * 60 * 1000
        else:
            return create_timestamp()

    @staticmethod
    def _create_int(**identity):
        if identity.get("num"):
            return identity.get("num")
        else:
            return 1

    @staticmethod
    def _create_float(**identity):
        if identity.get("num"):
            return identity.get("num") + 0.1
        else:
            return 1.1

    def _create_input(self, **identity):
        if identity.get("lack_must"):
            return getattr(GraphqlInterface(self.interface, self), identity.get("lamb"))(**identity)
        else:
            return GraphqlInterface(self.interface, self).generate_params(**identity)

    def _create_enum(self, **identity):
        enum_info = GraphqlInterface.get_interface_json(self.interface)
        return random.choice(enum_info["params"])

    def _create_jsonstring(self, **identity):
        if identity.get("lack_must"):
            return getattr(GraphqlInterface(self.interface, self), identity.get("lamb"))(**identity)
        else:
            return GraphqlInterface(self.interface, self).generate_params(**identity)

    # @staticmethod
    # def _create_upload(self, **identity):
    #     return None

    def __call__(self, **kwargs):
        return self._generate(**kwargs)


if __name__ == "__main__":
    '''
    identity 示例
    identity {
        "num" : 1, #  创建的默认后缀，按照数量递增，但是如果is_random为True那么无效
        "delay" : 10,# 时间戳的延后时间
        "no_optional" : False, # 控制没有选填项
        "is_random" : False, # 不生成随机字符串
        "list_len": 3 # 列表长度
        "no_none": True # 将所有为none的值全都pop掉
        
        ....
    }
    '''
    pass
