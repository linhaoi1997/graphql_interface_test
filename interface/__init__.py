import pytest
import os
from support import go_allure


def main(interface="interface/thing_test", is_clear_report=True):
    go_allure(is_clear_report)
    pro_dir = os.path.dirname(os.path.dirname(__file__))
    xml_path = pro_dir + "/output/report/xml/"
    test_dir = os.path.join(pro_dir, interface)
    # pytest.main(['-v', "-s", test_dir, "-k", "delete", '--alluredir', xml_path])
    pytest.main(['-v', "-s", test_dir, "-k", "not query and not delete", '--alluredir', xml_path])
    pytest.main(['-v', "-s", test_dir, "-k", "query", '--alluredir', xml_path])
    go_allure()


if __name__ == "__main__":
    test_interface = "interface/sparePart_test"
    test_is_clear_report = False
    main(test_interface, test_is_clear_report)
    # test_interface = "interface/thingMaintenanceRule_test"
    # test_is_clear_report = False
    # main(test_interface, test_is_clear_report)
