import os
import re


class GqlWriter(object):

    def __init__(self, gql_path, py_path, epic):
        self.query_type = None
        self.epic = epic
        self.gql_path = gql_path
        self.py_path = py_path
        self.interface_name, self.interface_name_cap, self.func_name, self.interface_title = self.get_interface_name()
        self.format_msg = self.get_format_message().format(
            interface_name=self.interface_name,
            interface_name_cap=self.interface_name_cap,
            func_name=self.func_name,
            interface_title=self.interface_title,
            epic=self.epic,
            query_type=self.query_type
        )
        self.write_file()

    def get_interface_name(self):
        with open(self.gql_path) as f:
            msg = f.readline()
        query_type, interface_name = re.search("(\w+)\s(\w+)\(.*", msg).groups()
        self.query_type = "queries" if query_type == "query" else "mutations"
        return interface_name, self.get_capital_string(interface_name, query_type), \
               self.get_func_name(interface_name, query_type), self.get_interface_title(interface_name, query_type)

    def write_file(self):
        file_name = "test_" + self.interface_title + '.py'
        file_path = os.path.join(self.py_path, file_name)
        print(file_path)
        if os.path.exists(file_path):
            print("file already exists pass")
        else:
            with open(file_path, "w") as f:
                f.write(self.format_msg)

    @staticmethod
    def get_capital_string(interface_name, query_type):
        if query_type == "query":
            return "Query" + interface_name[0].upper() + interface_name[1:]
        else:
            return interface_name[0].upper() + interface_name[1:]

    @staticmethod
    def get_func_name(interface_name, query_type):
        upper_list = []
        j = 0
        for i in range(len(interface_name)):
            if interface_name[i].isupper():
                upper_list.append(interface_name[j:i].lower())
                j = i
        upper_list.append(interface_name[j:].lower())
        if query_type == "query":
            upper_list.insert(0, 'query')
        return "_".join(upper_list)

    @staticmethod
    def get_interface_title(interface_name, query_type):
        if query_type == "query" and not interface_name.lower().startswith('export'):
            return "query" + GqlWriter.get_capital_string(interface_name, '')
        else:
            return interface_name

    @staticmethod
    def get_format_message():
        file_path = os.path.join(os.path.dirname(__file__), 'interface_format')
        with open(file_path, 'r') as f:
            msg = f.read()
        return msg


if __name__ == "__main__":
    test_path = "/Users/linhao/graphql/8061/queries/exportSparePartReceipts.gql"
    test_py_path = os.path.dirname(__file__)
    print(test_py_path)
    test = GqlWriter(test_path, test_py_path, "suibianxie")

    # 自动生成脚本/检查输入参数
