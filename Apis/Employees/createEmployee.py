from support import BaseApi


class CreateEmployee(BaseApi):
    def __init__(self, user=None):
        super(CreateEmployee, self).__init__("createEmployee", user)

    def create_employee(self, name, account, password, department_id=1):
        self.set_random_variables()
        self.variables.get("input").update(
            {
                "department": {"id": department_id},
                "status": "ACTIVATED",
                "account": account,
                "password": password,
                "name": name
            }
        )
        self.variables.get("input").pop("roles")
        return self.run()

    def init_employees(self):
        self.create_employee("发起人", "faqiren", "123456")
        self.create_employee("执行人", "zhixing", "123456")
        self.create_employee("审核人", "shenhe", "123456")
        self.create_employee("假的管理员", "admin_jia", "123456")
        self.create_employee("林", "test_lin", "123456")


if __name__ == '__main__':
    test = CreateEmployee()
    test.init_employees()
