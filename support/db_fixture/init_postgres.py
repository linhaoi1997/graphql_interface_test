from support.caps.read_yaml import get_web_information
from sqlalchemy import MetaData, create_engine, Table
from datetime import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


def get_struct_time():
    t = datetime.now()
    return datetime.fromtimestamp(t)


class DataInitExecuter(object):

    def __init__(self):
        url = 'postgresql://{}:{}@{}:{}/{}'
        db_information = get_web_information("db")
        url = url.format(*db_information)
        self.engine = create_engine(url, client_encoding='utf-8')
        self.metadata = MetaData(self.engine)

    def base_insert(self, table_name, values: dict):
        apply_info = Table(table_name, self.metadata, autoload=True)
        action = apply_info.insert().values(**values)
        result = self.engine.execute(action)
        print(result)


if __name__ == "__main__":
    import datetime

    data = DataInitExecuter()
    values = {
        "name": "python_auto_test",
        "created": get_struct_time(),
        "modified": get_struct_time(),
        "address": 'hangzhou1',
        'mail': "auto@auto.com",
        'phone': "15700000000",
        'manager_name': 'linhao',
        'type': "1"
    }
    data.base_insert('companies_company', values)
