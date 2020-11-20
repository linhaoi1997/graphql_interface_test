from support import run, BaseTestCase
from Apis.Things.exportThing import ExportThing


class TestExportThing(BaseTestCase):
    export_thing = ExportThing()

    def test_export_all(self):
        result = self.export_thing.export_things()
        self.assertCorrect(result)


if __name__ == "__main__":
    run(__file__)
