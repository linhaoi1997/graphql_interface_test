from support import FormStructApi
from Apis.Things.things import Things


class CreateSparePart(FormStructApi):
    def __init__(self, user=None):
        super(CreateSparePart, self).__init__("createSparePart", user)

    def create(self):
        self.set_random_variables()
        self.change_value("input.things", [{"id": Things().return_random_thing()} for i in range(2)])
        self.run()
        return self.result

    def create_with_no_optional(self):
        self.set_no_optional_var()
        return self.run()

    def return_spare_details(self):
        return self.variables["input"]["details"]
