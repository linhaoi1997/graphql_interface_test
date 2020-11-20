from support import FormStructApi


class CreateSparePart(FormStructApi):
    def __init__(self, user=None):
        super(CreateSparePart, self).__init__("createSparePart", user)

    def create(self):
        self.set_random_variables()
        return self.run()

    def create_with_no_optional(self):
        self.set_no_optional_var()
        return self.run()
