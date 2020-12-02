from support import FormStructApi
from Apis.Departments.departments import WorkShops
import datetime
import random


class CreateThing(FormStructApi):
    def __init__(self, user=None):
        super(CreateThing, self).__init__("createThing", user)

    def create_thing(self, **kwargs):
        self.set_random_variables()
        workshop = random.choice(WorkShops().query_and_return_ids())
        self.variables.get("input").update(
            {
                "attachments": [{"id": 1}, {"id": 2}],
                "images": [{"id": 1}, {"id": 2}],
                "repairContacts": [{"id": 1}],
                "department": {"id": workshop}
            }
        )
        self.variables.get("input").pop("spareParts")
        self.variables.get("input").pop("usedYear")
        self.variables.get("input").update(**kwargs)
        return self.run()

    def create_no_optional(self):
        self.variables = self.interface_generator.generate_params(no_optional=True, no_none=True, is_random=True)
        return self.run()

    def create_time_before(self, before_years):
        self.set_random_variables()
        days = int(365 * before_years)
        now = datetime.datetime.now()
        result = now - datetime.timedelta(days=days)
        return self.create_thing(activatedAt=int(result.timestamp() * 1000))
