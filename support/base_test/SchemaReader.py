from ..caps.read_yaml import config
from beeprint import pp
from ..tools import singleton
from ..data_maker.GraphqlClient import GraphqlClient

file_path = config.get_file_path("schema_graphql")
schema_path = config.get_file_path("schema")


@singleton
class SchemaReader(object):
    all_base_type = ("Int", "Float", "String", "ID", "Boolean", "Upload", "JSONString", "Timestamp")

    def __init__(self):
        self.resource = {}
        self.enum = self._enum()
        self.input = self._input()
        self.interfaces = self._query_param()
        self._input_second_treat()
        if self.find("formStructs"):
            try:
                self._change_form_struct()
            except Exception as e:
                print(e)
                print("可能是网络不通或者form structs接口发生错误，需要检查")

    def _query_param(self):
        all_query = self._find("Query")[0][1:]
        all_query.extend(self._find("Mutation")[0][1:])
        all_interfaces = []
        for interface in all_query:
            if "(" in interface:
                query_name, info = interface.split("(")[0:2]
                info, return_type = info.split(")")
                return_type = return_type.split(":")[1].strip()
                info = info.split(",")
                params = self._format_param(info)
                interface = {"name": query_name, "return_type": return_type, "params": params}
                all_interfaces.append(interface)
            elif ":" in interface:
                query_name, return_type = [i.strip() for i in interface.split(':')]
                interface = {"name": query_name, "return_type": return_type, "params": []}
                all_interfaces.append(interface)
        return all_interfaces

    def _type(self):
        all_query = self._find("type")

    def _enum(self):
        all_query = self._find("enum")
        all_enum = []
        for enum in all_query:
            name = enum.pop(0).split(" ")[1]
            params = enum
            all_enum.append({"name": name, "params": params})
        return all_enum

    def _input(self):
        all_query = self._find("input")
        all_input = []
        for _input in all_query:
            name = _input.pop(0).split(" ")[1]
            all_input.append({"name": name, "params_msg": _input})
        return all_input

    def _input_second_treat(self):
        for _input in self.input:
            _input["params"] = self._format_param(_input["params_msg"])
            for param in _input["params"]:
                if param.get("name") == "addition":
                    param["interface"] = _input["name"][6:-5] + "JsonString"
            _input.pop("params_msg")

    @staticmethod
    def _find(name):
        all_query = []
        with open(schema_path) as f:
            msg = f.readline()
            while msg:
                if name in msg and "{" in msg:
                    query = []
                    while "}" not in msg:
                        if '"""' not in msg and msg != "\n":
                            query.append(msg.strip())
                        msg = f.readline()
                    all_query.append(query)
                msg = f.readline()
        return all_query

    def _format_param(self, params_msg: list) -> dict:
        format_params = []
        for param in params_msg:
            format_param = {"name": [i.strip() for i in param.split(":")][0],
                            "type": [i.strip() for i in param.split(":")][1]}
            if format_param.get("type").endswith("!"):
                format_param['is_must'] = True
                format_param["type"] = format_param["type"][:-1]
            else:
                format_param["is_must"] = False
            if format_param["type"].endswith("]"):
                format_param['identity'] = "list"
                format_param["type"] = format_param["type"][1:-1]
            if format_param["type"].endswith("!"):
                format_param['inside_is_must'] = True
                format_param["type"] = format_param["type"][:-1]
            if format_param["type"] not in self.all_base_type:
                if self._judge_in(format_param["type"], self.enum):
                    format_param["interface"] = format_param["type"]
                    format_param["type"] = "enum"
                elif self._judge_in(format_param["type"], self.input):
                    format_param["interface"] = format_param["type"]
                    format_param["type"] = "input"
                else:
                    raise Exception("Unknown Type %s" % format_param["type"])
            format_params.append(format_param)
        return format_params

    @staticmethod
    def _judge_in(name, all_list: list):
        for _dict in all_list:
            if name == _dict["name"]:
                return True

    def find(self, name):
        for interface in self.interfaces:
            if name == interface["name"]:
                return interface
        for _input in self.input:
            if name == _input["name"]:
                return _input
        for enum in self.enum:
            if name == enum["name"]:
                return enum

    def get_all_interface_name(self):
        name = []
        for interface in self.interfaces:
            name.append(interface["name"])
        return name

    def set_users(self, user_name, use_interfaces):
        for interface_name in use_interfaces:
            for interface in self.interfaces:
                if interface.get("name") == interface_name:
                    if interface.get("allow_users"):
                        interface["allow_users"].append(user_name)
                    else:
                        interface["allow_users"] = [user_name]

    def _change_form_struct(self):
        # 发送请求查找所有表单的格式
        s = GraphqlClient(login=config.get_account("simple_user"))
        variables = {
            "isDraft": False
        }
        result = s.send_request("formStructs", variables).result["data"]["formStructs"]

        # create/update input 和返回的表单信息进行对应，在input中加入json input
        def create_addition_input(_form: dict):
            # 根据每个表单的信息来构建额外的输入参数
            base_name = "".join([i.title()[:-1] if i.endswith("s") else i.title() for i in _form["name"].split("_")])
            _input = {"name": base_name + "JsonString", "params": []}
            for _param in _form["customFields"]:
                # addition的内容和原表单区分开，原表单内容不可修改的不动
                # if _param.get("modifiable"):
                if True:
                    # 构造每个参数需要的的信息加入到resource中
                    # 参数含义记录
                    if _param.get("fieldName"):
                        real_name = _param.get("fieldName")
                    elif _param.get("colName"):
                        real_name = _param.get("colName")
                    else:
                        real_name = _param.get("title")
                    # 参数名称记录/是否必填记录
                    struct_param = {
                        "real_name": real_name,
                        "name": _param.get("fieldName") if _param.get("fieldName") else _param["id"],
                        "is_must": _param.get("required")
                    }
                    type_map = {
                        "TEXT": "String",
                        "CONTACT": "String",
                        "DATETIME": "TimeStamp",
                        "NUMBER": "Float",
                        "ATTACHMENT": "attachment",
                        "IMAGE": "attachment",
                        "SINGLE_SELECTION": "enum",
                        "MULTI_SELECTION": "enum",
                        "DESCRIPTION": "String"
                    }
                    struct_param["type"] = type_map.get(_param["type"])

                    # 需要特殊处理的类型
                    if _param["type"] == "TEXT":
                        if _param.get("wordCountLimit"):
                            struct_param["len"] = (_param["wordCountLimit"]["min"], _param["wordCountLimit"]["max"])
                    elif _param["type"] == "SINGLE_SELECTION":
                        self.enum.append({"name": "new" + _param["title"], "params": _param["candidates"]})
                        struct_param.update({"interface": "new" + _param["title"]})
                    elif _param["type"] == "MULTI_SELECTION":
                        self.enum.append({"name": "new" + _param["title"], "params": _param["candidates"]})
                        struct_param["identity"] = "list"
                        struct_param.update({"interface": "new" + _param["title"]})
                    elif _param["type"] in ("IMAGE", "ATTACHMENT"):
                        struct_param["identity"] = "list"
                        struct_param["is_file"] = True
                        struct_param["sizeLimit"] = _param["sizeLimit"]
                        if _param.get("countLimit"):
                            struct_param["countLimit"] = _param["countLimit"]
                            struct_param["identity"] = "list"
                    # 如果是原表单有的值，更新原表单信息，否则加到addition里
                    if _param.get("isOrigin"):
                        create_input = "Create" + base_name + "Input"
                        update_input = "Update" + base_name + "Input"
                        self._change_input(create_input, struct_param)
                        self._change_input(update_input, struct_param)
                    else:
                        _input["params"].append(struct_param)
            return _input

        for form in result:
            addition_input = create_addition_input(form)
            self.input.append(addition_input)

    def _change_input(self, input_name, struct_param):
        for _input in self.input:
            if _input["name"] == input_name:
                for num, param in enumerate(_input["params"]):
                    if param["name"] == struct_param["real_name"]:
                        interface = _input["params"][num].get("interface")
                        _type = _input["params"][num].get("type")
                        _input["params"][num] = struct_param
                        if struct_param['type'] != "enum":
                            _input["params"][num]["type"] = _type
                            _input["params"][num]["interface"] = interface


'''
enum 格式：{'name': 'FieldType','params': ['DESCRIPTION', 'TEXT', 
'DATETIME', 'NUMBER', 'CONTACT', 'IMAGE', 'ATTACHMENT', 'SINGLE_SELECTION', 'MULTI_SELECTION']},
input 格式
  {'name': 'CreateSparePartInput','params': [
      {
        'interface': 'SparePartType',
        'is_must': True,
        'name': 'type',
        'type': 'enum',
      },
      {
        'is_must': True,
        'name': 'model',
        'type': 'String',
      },
      {
        'is_must': False,
        'name': 'addition',
        'type': 'JSONString',
      },
    ],
  }
interface格式
{
    'name': 'thing',
    'params': [
      {
        'is_must': True,
        'name': 'id',
        'type': 'ID',
      },
    ],
    'return_type': 'Thing',
  },
'''
