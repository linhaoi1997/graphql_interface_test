import re
import collections

import argparse

parser = argparse.ArgumentParser(description='execute sql file')
parser.add_argument('-sql-file', '--file', required=True, dest='sql_file',
                    help='sql file to execute')
parser.add_argument('-dest-file', dest='dest_file', required=True,
                    help='destination dir path')
parser.add_argument('--no-data', dest='data', action="store_false", help='need data', default=True)
args = parser.parse_args()


class SqlReader(object):

    def __init__(self, file_path, data=True):
        with open(file_path, 'r') as f:
            self.msg = f.readlines()
        self.command_list = []
        self.collect_command()
        self.drop_foreign_key = DropForeignKey(self.command_list)
        self.recreate_data = RecreateData(self.command_list, data)
        self.set_val = SetVal(self.command_list, data)
        self.add_foreign_key = AddForeignKey(self.command_list)
        self.write_file = None

    def read_msgs(self):
        for i in self.command_list:
            print(i)

    def collect_command(self):
        command = ''
        for i in self.msg:
            i = i.strip().strip('\n')
            if i.startswith('-'):
                continue
            elif i.endswith(';'):
                command = command + ' ' + i
                self.command_list.append(command.strip())
                command = ''
            else:
                command += i

    def write_list_to_file(self, file_path, match_sql):
        data_list = match_sql.output()
        # beeprint.pp(data_list)
        if not self.write_file:
            self.write_file = open(file_path, 'w')
        for i in data_list:
            self.write_file.write(i + '\n')

    def write_to_file(self, file_path):
        self.write_list_to_file(file_path, self.drop_foreign_key)
        self.write_list_to_file(file_path, self.recreate_data)
        self.write_list_to_file(file_path, self.set_val)
        self.write_list_to_file(file_path, self.add_foreign_key)
        self.write_file.close()


class MatchSql(object):

    def __init__(self):
        self.command_list = []

    def collect_data(self, command_list: list, query_schema: str):
        for i in command_list:
            if re.match(query_schema, i) and "alembic_version" not in i:
                self.command_list.append(i)
                # print(i)

    def output(self):
        return self.command_list


class DropForeignKey(MatchSql):

    def __init__(self, command_list: list):
        self.schema = 'ALTER TABLE ONLY .+ ADD CONSTRAINT .+ FOREIGN KEY .+ REFERENCES public.+;'
        self.command_list = []
        self.collect_data(command_list, self.schema)
        self.turn_to_drop()
        # print(len(self.command_list))

    def turn_to_drop(self):
        for i in range(len(self.command_list)):
            self.command_list[i] = self.command_list[i].split('FOREIGN')[0]
            self.command_list[i] = self.command_list[i].replace('ADD', 'DROP') + ';'
        # for i in self.command_list:
        #     print(i)


class RecreateData(MatchSql):

    def __init__(self, command_list: list, data):
        self.data = data
        self.schema = 'INSERT INTO.+;'
        self.command_list = []
        self.collect_data(command_list, self.schema)
        self.table_information = self.collect_table()
        self.add_delete()
        # beeprint.pp(self.table_information)

    def collect_table(self):
        schema_str = 'INSERT INTO public\.([a-z_"]+)'
        table_information = collections.OrderedDict()
        for i in self.command_list:
            table_name = re.search(schema_str, i).group(1)
            if table_name not in table_information.keys():
                table_information[table_name] = [i]
            else:
                table_information[table_name].append(i)
        return table_information

    def add_delete(self):
        for i in self.table_information.keys():
            delete = 'TRUNCATE TABLE public.%s;' % i
            self.table_information[i].insert(0, delete)

    def output(self):
        command_list = []
        if self.data:
            for i in self.table_information.keys():
                command_list.extend(self.table_information[i])
        else:
            for i in self.table_information.keys():
                command_list.append(self.table_information[i][0])
        return command_list


class SetVal(MatchSql):

    def __init__(self, command_list: list, data):
        self.data = data
        self.schema = 'SELECT pg_catalog.setval.+;'
        self.command_list = []
        self.collect_data(command_list, self.schema)
        self._set_default()

    def _set_default(self):
        if self.data:
            pass
        else:
            for i in range(len(self.command_list)):
                self.command_list[i] = re.sub('\d+.+', "1, false);", self.command_list[i])


class AddForeignKey(MatchSql):

    def __init__(self, command_list: list):
        self.schema = 'ALTER TABLE ONLY .+ ADD CONSTRAINT .+ FOREIGN KEY .+ REFERENCES public.+;'
        self.command_list = []
        self.collect_data(command_list, self.schema)


def main():
    print("sql file is : " + args.sql_file)
    print("output file is : " + args.dest_file)
    print("Have data ? : " + str(args.data))
    sql = SqlReader(args.sql_file, args.data)
    sql.write_to_file(args.dest_file)


if __name__ == '__main__':
    main()
