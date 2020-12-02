from support import run, BaseTestCase
from Apis.Things.exportThing import ExportThing, ExportSpareParts, ExportSparePartOutbounds, ExportEmployees, \
    ExportSparePartReceipts, ExportSparePartStock, ExportSparePartSummary, ExportTaskSummary, \
    ExportThingInspectionRules, ExportThingInspections, ExportThingMaintenanceRules, ExportThingMaintenances, \
    ExportThingRepairs, ExportThingSummary


class TestExport(BaseTestCase):
    def test_ExportThingSummary(self):
        export = ExportThingSummary()
        result = export.export()
        self.assertCorrect(result)

    def test_ExportThingRepairs(self):
        export = ExportThingRepairs()
        result = export.export()
        self.assertCorrect(result)

    def test_ExportThingMaintenances(self):
        export = ExportThingMaintenances()
        result = export.export()
        self.assertCorrect(result)

    def test_ExportThingMaintenanceRules(self):
        export = ExportThingMaintenanceRules()
        result = export.export()
        self.assertCorrect(result)

    def test_ExportThingInspections(self):
        export = ExportThingInspections()
        result = export.export()
        self.assertCorrect(result)

    def test_ExportThingInspectionRules(self):
        export = ExportThingInspectionRules()
        result = export.export()
        self.assertCorrect(result)

    def test_ExportTaskSummary(self):
        export = ExportTaskSummary()
        result = export.export()
        self.assertCorrect(result)

    def test_ExportSparePartSummary(self):
        export = ExportSparePartSummary()
        result = export.export()
        self.assertCorrect(result)

    def test_ExportSparePartStock(self):
        export = ExportSparePartStock()
        result = export.export()
        self.assertCorrect(result)

    def test_export_SparePartReceipts(self):
        export = ExportSparePartReceipts()
        result = export.export()
        self.assertCorrect(result)

    def test_export_employees(self):
        export = ExportEmployees()
        result = export.export()
        self.assertCorrect(result)

    def test_export_thing(self):
        export = ExportThing()
        result = export.export()
        self.assertCorrect(result)

    def test_export_spare_parts(self):
        export = ExportSpareParts()
        result = export.export()
        self.assertCorrect(result)

    def test_export_spare_parts_outbounds(self):
        export = ExportSparePartOutbounds()
        result = export.export()
        self.assertCorrect(result)


if __name__ == "__main__":
    run(__file__)
