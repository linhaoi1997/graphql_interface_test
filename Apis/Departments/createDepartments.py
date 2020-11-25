from support import BaseApi


class CreateDepartment(BaseApi):
    def __init__(self, user=None):
        super(CreateDepartment, self).__init__("createDepartment", user)

    def create_department(self, name=None, parent=1, is_workshop=False):
        self.set_random_variables()
        var = {
            "parent": {"id": parent},
            "isWorkshop": is_workshop
        }
        if name:
            var["name"] = name
        self.variables.get("input").update(
            **var
        )
        self.run()
        self.pop_value("input.parent")

        return self.result
