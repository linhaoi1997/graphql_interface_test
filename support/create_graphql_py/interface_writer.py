from .single_gql_writer import GqlWriter
import os
from beeprint import pp


class InterfaceWriter(object):

    def __init__(self, interface_path, py_path, epics_list):
        self.interface_path = interface_path
        self.py_path = py_path
        if not os.path.exists(self.py_path):
            os.mkdir(self.py_path)
        self.epics_list = epics_list
        self.interface_dict = self.classify_interface()
        pp(self.interface_dict)

    def classify_interface(self):
        interface_dict = {}
        not_used = []
        for i in self.epics_list:
            interface_dict[i] = []
        all_interface = [
            os.path.join(
                self.interface_path + '/mutations', i
            ) for i in os.listdir(self.interface_path + '/mutations')
        ]

        all_interface.extend(
            [
                os.path.join(
                    self.interface_path + '/queries', i
                ) for i in os.listdir(self.interface_path + '/queries')
            ]
        )
        for i in all_interface:
            for j in interface_dict.keys():
                if i.split('.')[0].lower().endswith(j.lower()) or i.split('.')[0].lower().endswith(j.lower() + 's'):
                    interface_dict[j].append(i)
                    break
            else:
                not_used.append(i)
        pp(not_used)
        return interface_dict

    def execute_py_file(self):
        for i in self.interface_dict.keys():
            for interface in self.interface_dict[i]:
                py_path = os.path.join(self.py_path, i + '_test')
                if not os.path.exists(py_path):
                    os.mkdir(py_path)
                gql_writer = GqlWriter(interface, py_path, i)
                del gql_writer


if __name__ == "__main__":
    test_interface_path = "/Users/linhao/graphql/8061"
    test_py_path = os.path.dirname(__file__)
    test_epics = ['file', 'thing', 'sparePart', 'sparePartReceipt']
    test = InterfaceWriter(test_interface_path, test_py_path, test_epics)
