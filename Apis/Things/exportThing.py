from support import BaseApi, resource


class ExportThing(BaseApi):
    def __init__(self, user=None):
        super(ExportThing, self).__init__("exportThings", user)

    def export_things(self):
        thing_ids = resource.get_id("thing")
        variables = {
            "input": {
                "ids": thing_ids
            }
        }
        self.run(variables)
