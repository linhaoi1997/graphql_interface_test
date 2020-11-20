from support import BaseApi


class CreateDepartment(BaseApi):
    def __init__(self, user=None):
        super(CreateDepartment, self).__init__("createDepartment", user)

    def create_department(self, name=None, parent=None, is_workshop=False):
        self.set_random_variables()
        self.run(**{"parent": parent, is_workshop: False, "name": name})
