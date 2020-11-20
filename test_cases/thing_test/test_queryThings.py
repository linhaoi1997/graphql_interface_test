from Apis.Things import Things, CreateThing
from support import BaseTestCase, run
import pytest
import allure


class TestThings(BaseTestCase):
    thing = Things()
    names = ["name", "code", "model", "location", "manufacturer", "category", "factory", "status", "purpose"]

    @pytest.fixture(scope="class")
    def create_thing(self):
        create = CreateThing()
        create.create_thing()
        return create

    @allure.title("search by {name}")
    @pytest.mark.parametrize('name', names)
    def test_search_thing(self, name, create_thing):
        item = create_thing.find_first_deep_item(name)
        _id = self.thing.search(item)
        assert _id == create_thing.find_first_deep_item("id")


if __name__ == '__main__':
    run(__file__)
