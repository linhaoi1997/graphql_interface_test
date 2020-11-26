from support.base_test.base_api.SpecialApi import CreateApi


class CreateThingRepair(CreateApi):

    def __init__(self, user=None):
        super(CreateThingRepair, self).__init__("createThingRepair", user)

    def create_repair(self, thing_id):
        var = {"thing": {"id": thing_id}}
        return self.create(var)


class CreateThingRepairs(CreateApi):

    def __init__(self, user=None):
        super(CreateThingRepairs, self).__init__("createThingRepairs", user)
        self.ids = []

    def create_repairs(self, things_ids_list: list, is_draft=True):
        self.set_random_variables(list_len=len(things_ids_list))
        for i in range(len(things_ids_list)):
            self.change_value("input.data[%s].thing.id" % i, things_ids_list[i])
        fault_images = [{"id": i} for i in [1]]
        self.change_value("input.data[*].faultImages", fault_images)
        self.run()
        self.ids = self.find_from_result("$.data.%s.data[*].id" % self.api_name)
        return self.ids


if __name__ == '__main__':
    test = CreateThingRepairs()
    ids = test.create_repairs([1, 2, 3])
    print(ids)
