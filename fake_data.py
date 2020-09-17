from support.data_maker.DataFaker import DataFaker

if __name__ == '__main__':
    fake_data = DataFaker('createThing')
    fake_data.fake_data(21)
    fake_data = DataFaker('createSparePart')
    fake_data.fake_data(21)
    fake_data = DataFaker('createSparePartReceipt', is_id_increase=True)
    fake_data.fake_data(21)
    fake_data = DataFaker('createThingRepair', is_id_increase=True)
    fake_data.fake_data(21)
    fake_data = DataFaker('createSparePartOutbound', no_optional=True, is_id_increase=True)
    fake_data.fake_data(21)
    fake_data = DataFaker('createThingMaintenanceRule', is_id_increase=True, list_len=3)
    fake_data.fake_data(11)
    fake_data = DataFaker('createThingMaintenance', is_id_increase=True)
    fake_data.fake_data(11)