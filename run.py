import pytest
import os
from support import go_allure

if __name__ == "__main__":
    go_allure(True)
    pro_dir = os.path.dirname(__file__)
    xml_path = pro_dir + "/output/report/xml/"
    # pytest.main(['-v', "-s", "-k", "delete", '--alluredir', xml_path])
    pytest.main(['-v', "-s", "-k", "not query and not delete", '--alluredir', xml_path])
    # pytest.main(['-v', "-s", "-k", "employee", '--alluredir', xml_path])
    pytest.main(['-v', "-s", "test_cases", '--alluredir', xml_path])
    go_allure()
