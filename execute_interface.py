from support import InterfaceWriter, get_file_path
import os


def main():
    test_interface_path = get_file_path("schema_graphql")
    test_py_path = os.path.join(os.path.dirname(__file__), "interface")
    test_epics = ["department"]
    test = InterfaceWriter(test_interface_path, test_py_path, test_epics)
    test.execute_py_file()


if __name__ == "__main__":
    main()
