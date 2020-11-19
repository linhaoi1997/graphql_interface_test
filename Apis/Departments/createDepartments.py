from support import BaseApi


class CreateDepartments(BaseApi):

    def create_department(self, parent=None, is_workshop=False):
        self.run(**{"parent": parent, is_workshop: False})
