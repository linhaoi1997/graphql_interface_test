from ..caps.read_yaml import config
from ..tools.log import record
import re

SCHEMA_PATH = config.get_file_path("schema")


class InputSearcher(object):

    def __init__(self, input_name, **kwargs):
        self.sign = kwargs.get("sign", None)
        self.input_name = input_name
        self.input_msg = self._search()
        self.field_list = self._get_field_list()

    def _search(self):
        input_msg = []
        with open(SCHEMA_PATH) as f:
            if "input" in self.input_name.lower():
                while True:
                    msg = f.readline()
                    if not msg:
                        break
                    # 遇到正确的input把整个input段都截取出来
                    if self.input_name.lower() + ' {' in msg.lower():
                        # 截取开始
                        input_msg.append(msg)
                        while "}" not in msg:
                            msg = f.readline()
                            input_msg.append(msg)
                        break
            else:
                while True:
                    msg = f.readline()
                    if not msg:
                        break
                    if re.search("%s\(.*\)" % self.input_name, msg):
                        input_msg = msg.split("(")[1].split(")")[0].split(",")
                        break
        if not input_msg:
            record("no {input} found in schema".format(input=self.input_name))
            # raise TypeError
        return input_msg

    def _get_field_list(self):
        field_list = []
        for msg in self.input_msg:
            if ":" in msg:
                field_list.append(Field(msg))
        return field_list

    # def __next__(self):
    #     return iter(self.field_list)

    def __iter__(self):
        return iter(self.field_list)

    def get_json(self):
        result = {"name": self.input_name, "allow_user": "simple_user", "param": []}
        for field in self.field_list:
            result["param"].append(field.get_json())
        return result


class Field(object):

    def __init__(self, msg: str):
        self.msg = msg
        self.is_must = False
        self.identity = 'variables'
        self.input_searcher = None
        self.var_name, self.var_type = self._analysis_type()
        self.real_var_type = self.format_var_type(self.var_type)
        self._get_input()
        self.len = self._get_len()

    def _get_len(self):
        return None

    def _analysis_type(self):
        var_name, var_type = self.msg.strip().split(":")
        var_name = var_name.strip()
        var_type = var_type.strip()
        if var_type.endswith("!"):
            self.is_must = True
        if var_type.startswith('['):
            if "input" in var_type.lower():
                self.identity = "list_input"
            else:
                self.identity = "list"
        elif "input" in var_type.lower():
            self.identity = "input"
        return var_name, var_type

    def _get_input(self):
        if "input" in self.identity:
            self.input_searcher = InputSearcher(self.real_var_type, sign=self.var_name)

    @staticmethod
    def format_var_type(var_type):
        if var_type.endswith('!'):
            var_type = var_type[:-1]
        if var_type.startswith("["):
            var_type = var_type[1:-1]
        if var_type.endswith('!'):
            var_type = var_type[:-1]
        return var_type

    def get_json(self):
        interface = self.input_searcher.input_name if self.input_searcher else None
        if interface and "ID" not in interface:
            var_type = "input"
        elif self.real_var_type.endswith("Input"):
            var_type = self.real_var_type[:-5]
        else:
            var_type = self.real_var_type
        result = {
            "input_name": self.var_name,
            "type": var_type,
            "is_must": self.is_must,
            "identity": self.identity,
            "interface": interface,
            "len": self.len
        }
        return result
