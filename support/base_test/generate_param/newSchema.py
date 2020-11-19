from support.caps.read_yaml import config
from support.tools import pformat
import re

schema_path = config.get_file_path("schema")


class BaseType(object):

    def __init__(self, name):
        self.name = name
        self.children = []

    def _find_all(self, msg, name=None):
        if name is None:
            name = self.name
        index = 0
        result = []
        while index <= len(msg) - len(name):
            if msg[index] == name[0] and msg[index - 1] == "\n":
                if msg[index:index + len(name)] == name:
                    result.append(index + len(name) + 1)
            index += 1
        return result

    @staticmethod
    def find_next_symbol(symbol_a, symbol_b, msg, index):
        save = 1
        index += 1
        while index <= len(msg):
            if msg[index] == symbol_a:
                save += 1
            elif msg[index] == symbol_b:
                save -= 1
                if save == 0:
                    break
            index += 1
        return index

    @staticmethod
    def _handle(small_msg):
        result = []
        useless_str = ["\n", " ", "", ":"]
        f_index = 0
        b_index = 0
        while b_index < len(small_msg):
            if small_msg[b_index] in useless_str:
                if b_index != f_index and small_msg[f_index + 1:b_index] not in useless_str:
                    result.append(small_msg[f_index + 1:b_index])
                f_index = b_index
            b_index += 1
        return result

    def find_all(self, msg):
        all_index = self._find_all(msg)
        for i in all_index:
            j = i + 1
            result = {}
            while msg[j] not in ['{', "\n"]:
                j += 1
            result["name"] = msg[i:j - 1]
            end_index = self.find_next_symbol("{", "}", msg, j)
            result["value"] = self._handle(msg[j:end_index])
            self.children.append(result)

    def find_all_str(self, msg, name):
        all_index = self._find_all(msg, name)
        f = all_index[0]
        b = self.find_next_symbol("{", "}", msg, f)
        return msg[f:b]


class Enum(object):
    def __init__(self, name, value_list):
        self.name = name
        self.value_list = value_list


class Enums(BaseType):
    def __init__(self, msg):
        super(Enums, self).__init__("enum")
        self.find_all(msg)
        self.enum = []
        for child in self.children:
            self.enum.append(Enum(child["name"], child["value"]))

    def __getattr__(self, item):
        for enum in self.enum:
            if enum.name == item:
                return enum

    def add_enum(self, enum):
        self.enum.append(enum)


class Input(object):
    def __init__(self, name, param_information_list=None):
        self.name = name
        self.params = []
        # 从schema读取    if param_information_list:
        if param_information_list:
            self._handle(param_information_list)

    def _handle(self, param_information_list):
        index = 0
        while index < len(param_information_list):
            if "\"" not in param_information_list[index]:
                self.params.append(Param(param_information_list[index], param_information_list[index + 1]))
                index += 2
            else:
                index += 1

    def add_param(self, param):
        self.params.append(param)

    def update_param(self, custom_fields: list, schema):
        # 先改变addition的属性
        name = self.name + "JSONString"
        self.addition.type = name
        # 给schema加入一个input
        new_input = Input(name)
        for i in custom_fields:
            # 如果param存在
            if self.get_param(i["fieldName"]):
                param = self.get_param(i["fieldName"])
                param.handle_for_form_struct(i, schema)
            else:
                new_input.add_param(Param(i["id"], self_define_info=i, schema=schema))
        schema.add_input(new_input)

    def __repr__(self):
        test_str = "input name %s ,params:\n" % self.name
        for param in self.params:
            test_str = test_str + "\t" + pformat(param)
        return test_str

    def get_param(self, item):
        for param in self.params:
            if param.name == item:
                return param

    def __getattr__(self, item):
        return self.get_param(item)


class Param(object):

    def __init__(self, name, _type: str = None, self_define_info=None, schema=None):
        self.name = name
        self._type = _type
        self.is_must = False
        self.is_list = False
        self.is_list_can_empty = True
        self.type = None
        self.real_name = self.name
        if _type:
            self._handle()
        else:
            self.handle_for_form_struct(self_define_info, schema)

    def _handle(self):
        test_type = self._type
        if test_type.endswith("!"):
            test_type = test_type[:-1]
            self.is_must = True
        if test_type.endswith("]"):
            test_type = test_type[1:-1]
            self.is_list = True
        if test_type.endswith("!"):
            test_type = test_type[:-1]
            self.is_list_can_empty = False
        all_base_type = ("Int", "Float", "String", "ID", "Boolean", "Upload", "JSONString", "Timestamp")
        self.type = test_type

    def handle_for_form_struct(self, define_info: dict, schema):
        type_map = {
            "TEXT": "String", "SINGLE_SELECTION": "SINGLE_SELECTION", "MULTI_SELECTION": "MULTI_SELECTION",
            "NUMBER": "Float", "ATTACHMENT": "IDInput", "IMAGE": "IDInput"
        }
        if define_info.get("fieldName"):
            self.name = define_info.get("fieldName")
            self.real_name = self.name
        else:
            self.name = define_info.get("id")
            self.real_name = define_info.get("title")
        self.type = type_map[define_info.get("type")]
        self.is_must = define_info.get("required")
        if self.type in ("SINGLE_SELECTION", "MULTI_SELECTION"):
            schema.add_enum(Enum(self.name, define_info.get("candidates")))
            if self.type == "MULTI_SELECTION":
                self.is_list = True
            self.type = self.name

    def __repr__(self):
        return "Param name %s ,type %s, is_must %s, is_list %s" % (self.name, self.type, self.is_must, self.is_list)


class Inputs(BaseType):
    def __init__(self, msg):
        super(Inputs, self).__init__("input")
        self.find_all(msg)
        self.input = []
        for child in self.children:
            self.input.append(Input(child["name"], child["value"]))

    def __getattr__(self, item):
        for _input in self.input:
            if _input.name == item:
                return _input

    def add_input(self, _input: Input):
        self.input.append(_input)


class Interface(object):
    def __init__(self, name, param, return_type):
        self.name = name
        self.params = []
        if param:
            for _param in [i.strip() for i in param[1:-1].split(",")]:
                __param = Param(*[i.strip() for i in _param.split(":")])
                if __param.name == "input":
                    self.input = __param.type
                self.params.append(__param)
        self.return_type = return_type

    def __repr__(self):
        test_str = "test_cases name %s ,params:\n" % self.name
        for param in self.params:
            test_str = test_str + "\t" + pformat(param)
        return test_str


class Interfaces(BaseType):
    def __init__(self, msg):
        super(Interfaces, self).__init__("interfaces")
        query = self.find_all_str(msg, "type Query")
        mutation = self.find_all_str(msg, "type Mutation")
        self.interface = []
        children = re.findall("(\w+)(\(.*\))?: (\[?\w+!?\]?!?)", query)
        children.extend(re.findall("(\w+)(\(.*\))?: (\[?\w+!?\]?!?)", mutation))
        for i in children:
            self.interface.append(Interface(*i))

    def __getattr__(self, item):
        for i in self.interface:
            if i.name == item:
                return i


class Schema(object):

    def __init__(self, _schema_path=schema_path):
        with open(_schema_path, "r") as f:
            msg = f.read()
        self.msg = msg
        self.enum = Enums(self.msg)
        self.input = Inputs(self.msg)
        self.interfaces = Interfaces(self.msg)
        self.add_input(Input("JSONString"))

    def __getattr__(self, item):
        if getattr(self.interfaces, item):
            return getattr(self.interfaces, item)
        elif getattr(self.input, item):
            return getattr(self.input, item)
        elif getattr(self.enum, item):
            return getattr(self.enum, item)

    def add_input(self, _input: Input):
        self.input.add_input(_input)

    def add_enum(self, enum: Enum):
        self.enum.add_enum(enum)


base_schema = Schema()
all_input = base_schema.input

if __name__ == '__main__':
    print(base_schema.interfaces)
