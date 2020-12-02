from Apis.SpareParts.createSpareParts import CreateSparePart
from support import run, BaseTestCase
import allure
import pytest


class TestCreateSparePart(BaseTestCase):
    spare_part = CreateSparePart()
    query_name = spare_part.api_name

    @allure.title("以完整表单创建")
    def test_create_all(self):
        result = self.spare_part.create()
        self.assertCreate(self.spare_part.variables, result)

    @allure.title("以必填项表单创建")
    def test_create_no_optional(self):
        result = self.spare_part.create_with_no_optional()
        self.assertCreate(self.spare_part.variables, result)

    @pytest.mark.xfail
    @allure.title("不能创建相同的sap编码")
    def test_create_same(self):
        result = self.spare_part.run()


if __name__ == '__main__':
    run(__file__)
