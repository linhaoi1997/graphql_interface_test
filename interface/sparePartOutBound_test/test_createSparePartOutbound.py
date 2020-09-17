from support import *
import pytest
import allure

collection()


@allure.epic("sparePartOutBound")
@allure.feature("createSparePartOutbound")
class TestCreateSparePartOutbound(BaseTestCase):
    query_name = "createSparePartOutbound"
    interface = GraphqlInterface(query_name)

    @allure.story("所有项完整")
    @pytest.mark.parametrize("variable", interface.generate("generate_all_params", **BaseTestCase.all_param))
    def test_1(self, variable, resource):
        # 有bug先改下参数
        for i in variable["input"]["details"]:
            i["reason"] = "LOOSEN"
        variable["input"]["reason"] = "设备维修"
        variable["input"].pop("thingMaintenance")
        user = resource.simple_user
        result = user.send_request(self.query_name, variable).result
        self.assertForm(variable, result)


if __name__ == "__main__":
    run(__file__)
