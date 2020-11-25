from Apis.Departments.createDepartments import CreateDepartment
from support import run, BaseTestCase
import allure


class TestCreateDepartment(BaseTestCase):
    create_department = CreateDepartment()

    @allure.title("创建车间")
    def test_create_with_workshop(self):
        result = self.create_department.create_department(is_workshop=True)
        self.assertCreate(self.create_department.variables, result)
        with allure.step("在这个车间底下不能再创建车间"):
            _id = self.create_department.find_first_deep_item("id")
            result = self.create_department.create_department(parent=_id, is_workshop=True)
            self.assertError(result)

    @allure.title("不创建车间")
    def test_create_without_workshop(self):
        result = self.create_department.create_department()
        self.assertCreate(self.create_department.variables, result)
        with allure.step("在这个车间底下能再创建车间"):
            _id = self.create_department.find_first_deep_item("id")
            result = self.create_department.create_department(parent=_id, is_workshop=True)
            self.assertCorrect(result)


if __name__ == '__main__':
    run(__file__)
