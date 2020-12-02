from support import BaseApi, create_timestamp
from Apis.Things.things import Things
from Apis.SpareParts.querySpareParts import QuerySpareParts
from Apis.SpareParts.querySparePartStocks import QuerySparePartStocks, QuerySparePartReceipts, QuerySparePartOutbounds
from Apis.thingRepairs.thingRepairs import QueryThingRepairs
from Apis.thingInspections.queryThingInspectionRules import QueryThingInspectionRules
from Apis.thingInspections.queryInspection import QueryInspections
from Apis.thingMaintenances.queryThingMaintenanceRules import QueryThingMaintenanceRules
from Apis.thingMaintenances.queryThingMaintenance import QueryMaintenances
from Apis.Employees.Role import Employees


class ExportTaskSummary(BaseApi):
    def __init__(self, user=None):
        super(ExportTaskSummary, self).__init__("exportTaskSummary", user)

    def export(self):
        variables = {
            "end": create_timestamp(),
            "start": create_timestamp(before=24 * 60 * 7)
        }
        return self.run(variables)


class ExportSparePartSummary(BaseApi):
    def __init__(self, user=None):
        super(ExportSparePartSummary, self).__init__("exportSparePartSummary", user)

    def export(self):
        variables = {
            "end": create_timestamp(),
            "start": create_timestamp(before=24 * 60 * 7)
        }
        return self.run(variables)


class ExportThingSummary(BaseApi):
    def __init__(self, user=None):
        super(ExportThingSummary, self).__init__("exportThingSummary", user)

    def export(self):
        variables = {}
        return self.run(variables)


class ExportEmployees(BaseApi):
    def __init__(self, user=None):
        super(ExportEmployees, self).__init__("exportEmployees", user)

    def export(self):
        _ids = Employees().query_and_return_ids()
        variables = {
            "input": {
                "ids": _ids
            }
        }
        return self.run(variables)


class ExportThingMaintenances(BaseApi):
    def __init__(self, user=None):
        super(ExportThingMaintenances, self).__init__("exportThingMaintenances", user)

    def export(self):
        _ids = QueryMaintenances().query_and_return_ids()
        variables = {
            "input": {
                "ids": _ids
            }
        }
        return self.run(variables)


class ExportThing(BaseApi):
    def __init__(self, user=None):
        super(ExportThing, self).__init__("exportThings", user)

    def export(self):
        thing_ids = Things().query_and_return_ids()
        variables = {
            "input": {
                "ids": thing_ids
            }
        }
        return self.run(variables)


class ExportSpareParts(BaseApi):
    def __init__(self, user=None):
        super(ExportSpareParts, self).__init__("exportSpareParts", user)

    def export(self):
        _ids = QuerySpareParts().query_and_return_ids()
        variables = {
            "input": {
                "ids": _ids
            }
        }
        return self.run(variables)


class ExportSparePartStock(BaseApi):
    def __init__(self, user=None):
        super(ExportSparePartStock, self).__init__("exportSparePartStock", user)

    def export(self):
        _ids = QuerySparePartStocks().query_and_return_ids()
        variables = {
            "input": {
                "ids": _ids
            }
        }
        return self.run(variables)


class ExportSparePartReceipts(BaseApi):
    def __init__(self, user=None):
        super(ExportSparePartReceipts, self).__init__("exportSparePartReceipts", user)

    def export(self):
        _ids = QuerySparePartReceipts().query_and_return_ids()
        variables = {
            "input": {
                "ids": _ids
            }
        }
        return self.run(variables)


class ExportSparePartOutbounds(BaseApi):
    def __init__(self, user=None):
        super(ExportSparePartOutbounds, self).__init__("exportSparePartOutbounds", user)

    def export(self):
        _ids = QuerySparePartOutbounds().query_and_return_ids()
        variables = {
            "input": {
                "ids": _ids
            }
        }
        return self.run(variables)


class ExportThingRepairs(BaseApi):
    def __init__(self, user=None):
        super(ExportThingRepairs, self).__init__("exportThingRepairs", user)

    def export(self):
        _ids = QueryThingRepairs().query_and_return_ids()
        variables = {
            "input": {
                "ids": _ids
            }
        }
        return self.run(variables)


class ExportThingInspectionRules(BaseApi):
    def __init__(self, user=None):
        super(ExportThingInspectionRules, self).__init__("exportThingInspectionRules", user)

    def export(self):
        _ids = QueryThingInspectionRules().query_and_return_ids()
        variables = {
            "input": {
                "ids": _ids
            }
        }
        return self.run(variables)


class ExportThingInspections(BaseApi):
    def __init__(self, user=None):
        super(ExportThingInspections, self).__init__("exportThingInspections", user)

    def export(self):
        _ids = QueryInspections().query_and_return_ids()
        variables = {
            "input": {
                "ids": _ids
            }
        }
        return self.run(variables)


class ExportThingMaintenanceRules(BaseApi):
    def __init__(self, user=None):
        super(ExportThingMaintenanceRules, self).__init__("exportThingMaintenanceRules", user)

    def export(self):
        _ids = QueryThingMaintenanceRules().query_and_return_ids()
        variables = {
            "input": {
                "ids": _ids
            }
        }
        return self.run(variables)
