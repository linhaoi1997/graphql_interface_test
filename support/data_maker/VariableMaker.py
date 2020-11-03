from .InputSearcher import InputSearcher, Field
from ..tools.tools import create_timestamp
from .JsonSetter import JsonSetter
from copy import deepcopy
import random
from ..caps.read_yaml import config

SCHEMA_PATH = config.get_file_path("schema")


class TypeSearcher(object):
    def __init__(self, type_name):
        self.type_name = type_name
        self.type_msg = self._search()
        self.msg = self._analysis_msg()

    def _search(self):
        input_msg = []
        with open(SCHEMA_PATH) as f:
            while True:
                msg = f.readline()
                if not msg:
                    break
                # 遇到正确的input把整个input段都截取出来
                if self.type_name.lower() + ' {' in msg.lower():
                    # 截取开始
                    input_msg.append(msg)
                    while "}" not in msg:
                        msg = f.readline()
                        input_msg.append(msg)
                    break
        if not input_msg:
            print("no {input} found in schema".format(input=self.type_name))
            raise TypeError
        return input_msg

    def _analysis_msg(self):
        msg = []
        type_msg = self.type_msg
        if "enum" in type_msg[0]:
            self.type = "enum"
            for i in type_msg[1:-1]:
                msg.append(i.strip())
        elif "type" in type_msg[0]:
            self.type = type_msg[0].split(" ")[1]
            for i in type_msg[1:-1]:
                if ":" in i:
                    msg.append(i.strip().split(":")[0])
        else:
            print("unknown type")
            raise TypeError
        return msg


class Variable(object):

    def __init__(self, identity, list_len=1):
        self.list_len = list_len
        self.identity = list if "list" in identity else None
        if "list" in identity:
            self._variable = []
        else:
            self._variable = None

    @property
    def variable(self):
        return self._variable

    @variable.setter
    def variable(self, var):
        if self.identity == list and isinstance(var, VariableMaker):
            n = 1
            while True:
                if n <= self.list_len:
                    self._variable.append(deepcopy(var.variables))
                    next(var)
                    n += 1
                else:
                    break
        elif isinstance(var, VariableMaker):
            self._variable = var.variables
        else:
            self._variable = var


class VariableMaker(object):

    def __init__(self, input_searcher: InputSearcher, **kwargs):
        '''
        :param is_id_increase: 所有id自增,默认false.
        :type rule: bool

        :param no_optional: 不是必填项的所有参数都为None,默认false
        :type rule: bool

        :param rule: 使用字典指定某个路径下的值应该是多少
        :type rule: dict

        :param list_len: 指定列表型的值长度是多少
        :type list_len: int
        '''
        self.list_len = kwargs.get("list_len", 1)
        self.rule = kwargs.get("rule", None)
        self.is_id_increase = kwargs.get("is_id_increase", False)
        self.no_optional = kwargs.get("no_optional", False)
        self.num = kwargs.get("num", 1)
        self.variables = {}
        self.input_searcher = input_searcher
        self._add_argument(input_searcher)

    def _add_single_argument(self, field: Field):

        def call_str(test_var_name, test_num):
            return test_var_name + "_" + "0" * (3 - len(test_num)) + str(test_num)

        num = str(self.num)
        var_name = field.var_name
        real_var_type = field.real_var_type
        identity = field.identity
        var = Variable(identity, self.list_len)
        if self.no_optional and not field.is_must:
            var.variable = None
        elif "String" == real_var_type:
            var.variable = call_str(var_name, num)
        elif "Timestamp" == real_var_type:
            var.variable = create_timestamp()
        elif "ID" == real_var_type:
            if self.is_id_increase:
                var.variable = self.num
            else:
                var.variable = 1
        elif "Int" == real_var_type:
            var.variable = self.num
        elif "Float" == real_var_type:
            var.variable = self.num + 0.1
        elif "input" in identity:
            var.variable = VariableMaker(
                field.input_searcher, num=self.num,
                is_id_increase=self.is_id_increase
            )
        else:
            var.variable = random.choice(TypeSearcher(real_var_type).msg)
        self.variables[var_name] = var.variable

    def _add_argument(self, input_searcher):
        for field in input_searcher:
            self._add_single_argument(field)
        if self.rule:
            self.update_of_rule()
        self.real_variables = {"input": self.variables}

    def update_of_rule(self):
        for json_path, value in self.rule.items():
            test = JsonSetter(json_path)
            test.set(self.variables, value)

    def __next__(self):
        self.num += 1
        self._add_argument(self.input_searcher)
