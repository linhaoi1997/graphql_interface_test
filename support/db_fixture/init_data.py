import psycopg2
from support.tools import record
from support.caps.read_yaml import config


class PostgresConn(object):

    def __init__(self, database):
        self.user, self.password, self.host, self.port = config.get_web_information('db')
        self.database = database
        self.conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.conn.cursor()

    def query(self, query):
        # query_str = "SELECT * FROM user_role WHERE role_id =2;"
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()

    def update(self, update):
        self.cursor.execute(update)
        self.conn.commit()

    def execute_file(self, file_path):
        with open(file_path) as f:
            msg = f.readlines()
            execute = ''
            for i in msg:
                i = i.strip().split('\n')[0]
                if i.startswith('-'):
                    continue
                elif i.endswith(';'):
                    execute = execute + ' ' + i
                    try:
                        self.conn.commit()
                        self.cursor.execute(execute)
                        self.conn.commit()
                    except Exception as e:
                        print(e)
                        print(execute)
                    finally:
                        execute = ''
                elif not execute.endswith(';'):
                    execute += i

    def get_id(self, table_name, id_name="id"):
        query = "select %s from %s" % (id_name, table_name)
        return [i[0] for i in self.query(query)]

    def __del__(self):
        self.conn.commit()
        self.conn.close()
        print(self.database + ' close')


class PlatformDataSearcher(object):

    def __init__(self, name):
        self.authen = PostgresConn('authen-' + name)
        self.passport = PostgresConn('passport-base-' + name)
        self.tpmain = PostgresConn('tpmain-' + name)

    def query_staff(self, company_name='teletraan', role_id=3):
        query_str = "SELECT user_id FROM user_role WHERE role_id =%s;" % role_id
        fetch = self.authen.query(query_str)
        data_str = self.collect_data(fetch)
        query_str = 'SELECT "user"."account","user"."id" FROM "user" INNER JOIN company ON "user".company_id=company."id" WHERE "user"."id" in %s' % (
            data_str)
        # query_str = 'SELECT * FROM "user"'
        fetch = self.tpmain.query(query_str)
        return fetch

    def update_passport_user_id(self, user_id, account):
        update = "update users_user set username = '%s' where id ='%s'" % (account, user_id)
        self.passport.update(update)
        return True

    @staticmethod
    def collect_data(data):
        data_list = [i[0] for i in data]
        data_str = str(tuple(data_list))
        return data_str


def execute_sql(database, sql_path):
    conn = PostgresConn(database)
    conn.execute_file(sql_path)


def init_data(sql=None):
    record('start init database')
    db_list = config.get_web_information('db_list')
    for db in db_list:
        if not sql:
            eam_sql = config.get_file_path(db + '_sql')
            print(eam_sql)
        else:
            eam_sql = config.get_file_path(sql)
        record('start init %s' % db)
        execute_sql(db, eam_sql)


if __name__ == "__main__":
    print(config.get_web_information("db"))
    test = PostgresConn("eam-sleemon")
    print(test.get_id("things"))
    # init_data(None)
