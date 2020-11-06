from support.base_test.base_api.BaseApi import BaseApi

form_struct = BaseApi("formStruct")
form_struct.variables = {"name": "things", "isDraft": False}


def format_s(name: str):
    if name.endswith("s"):
        return name[:-1]
    return name


def format_name(name: str):
    all_name = (
        "spare_part_outbounds", "spare_part_receipts", "spare_parts", "thing_inspection_rules",
        "thing_inspections", "thing_inspections_feedback",
        "thing_maintenance", "thing_maintenance_feedback", "thing_maintenance_rules", "thing_repairs",
        "thing_repairs_feedback", "things"
    )
    if name.endswith("Input"):
        name = name[:-5]
    if name.startswith("Create") or name.startswith("Update"):
        name = name[6:]
    name = name.lower()
    for i in all_name:
        if "".join([format_s(j) for j in i.split("_")]) == name:
            return i
    raise Exception("没有找到对应表单")


class FormStructApi(BaseApi):

    def run(self, is_change_struct=False):
        if is_change_struct:
            self.change_struct()
            self.set_random_variables()
        self.result = self.user.send_request(self.api_name, self.variables).result

    def change_struct(self):
        interface = getattr(self.schema, self.api_name)
        _input = getattr(self.schema, interface.input)

        form_struct.variables["name"] = format_name(_input.name)
        form_struct.run()
        result = form_struct.result
        custom_fields = result["data"]["formStruct"]["customFields"]
        _input.update_param(custom_fields, self.schema)
        print(self.interface_generator.generate_params())


if __name__ == '__main__':
    test = FormStructApi("createSparePart")
    test.change_struct()
