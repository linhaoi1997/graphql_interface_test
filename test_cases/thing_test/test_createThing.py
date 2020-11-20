from Apis.Things.createThing import CreateThing
from support import BaseTestCase, run
import pytest
import allure


class TestCreateThing(BaseTestCase):
    create_thing = CreateThing()
    query_name = create_thing.api_name

    def test_create_all(self):
        result = self.create_thing.create_thing()
        self.assertCreate(self.create_thing.variables, result)

    def test_create_no_optional(self):
        result = self.create_thing.create_no_optional()
        self.assertCreate(self.create_thing.variables, result)

    @pytest.mark.parametrize('year', [0.5, 1, 1.5])
    def test_half_year(self, year):
        result = self.create_thing.create_time_before(year)
        self.assertCreate(self.create_thing.variables, result)
        self.assertJsonResponseEqual("$..usedYear", result, year)

    @allure.title("1.8年")
    def test_1_8_year(self):
        result = self.create_thing.create_time_before(1.8)
        self.assertCreate(self.create_thing.variables, result)
        self.assertJsonResponseEqual("$..usedYear", result, 1.8)


if __name__ == '__main__':
    run(__file__)
