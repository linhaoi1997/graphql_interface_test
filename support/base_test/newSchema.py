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
            result["name"] = msg[i:j-1]
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


class Input(object):
    def __init__(self, name, param_information_list):
        self.name = name
        self.params = []
        self._handle(param_information_list)

    def _handle(self, param_information_list):
        index = 0
        while index < len(param_information_list):
            if "\"" not in param_information_list[index]:
                self.params.append(Param(param_information_list[index], param_information_list[index + 1]))
                index += 2
            else:
                index += 1

    def __repr__(self):
        test_str = "input name %s ,params:\n" % self.name
        for param in self.params:
            test_str = test_str + "\t" + pformat(param)
        return test_str

    def __getattr__(self, item):
        for param in self.params:
            if param.name == item:
                return param


class Param(object):

    def __init__(self, name, _type: str):
        self.name = name
        self._type = _type
        self.is_must = False
        self.is_list = False
        self.is_list_can_empty = True
        self.type = None
        self._handle()

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


class Interface(object):
    def __init__(self, name, param, return_type):
        self.name = name
        self.params = []
        if param:
            for _param in [i.strip() for i in param[1:-1].split(",")]:
                self.params.append(Param(*[i.strip() for i in _param.split(":")]))
        self.return_type = return_type


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

    def __getattr__(self, item):
        if getattr(self.interfaces, item):
            return getattr(self.interfaces, item)
        elif getattr(self.input, item):
            return getattr(self.input, item)
        elif getattr(self.enum, item):
            return getattr(self.enum, item)


eam_schema = Schema()
all_input = eam_schema.input

if __name__ == '__main__':
    print(eam_schema.interfaces)
