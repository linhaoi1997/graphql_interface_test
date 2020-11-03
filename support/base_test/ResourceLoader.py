from ..caps.read_yaml import config
from ..tools import singleton
from .SchemaReader import SchemaReader
from ..data_maker import GraphqlClient
import random

interface_info = SchemaReader()


@singleton
class ResourceLoader(object):
    '''
    id对应格式：
    ('Thing', {'value': ['e081658a-882d-42e4-8419-01abbcc58d9e', 'e181658a-882d-42e4-8419-01abbcc58d9e'], 'num': 0})
    id_map对应格式
    {'thing': 'createThing'}
    users对应格式
    {'name': 'simple_user', 'client': <support.base_test.ResourceLoader.User object at 0x109e4dc18>}
    '''

    def __init__(self):
        self.interface = interface_info
        self.users = UserLoader()
        self.id_map = IdMap()
        self.id = {}
        self.all = [i["name"] for i in self.interface.interfaces]
        self._num = 0

    def __getattr__(self, item):
        if "user" in item:
            return getattr(self.users, item)
        else:
            return self.interface.find(item)

    def import_id(self, id_map: dict):
        for name, _id in id_map.items():
            self.id[name] = {"value": _id, "num": 0}

    def create(self, query, variables, is_collect=False):
        if is_collect:
            for id_info in self.users.create(query, variables):
                id_name, id_value = id_info
                if self.id.get(id_name):
                    self.id[id_name]["value"].append(id_value)
                else:
                    self.id[id_name] = {"value": [id_value]}
                    self.id[id_name]["num"] = 0
        else:
            result = {}
            id_list = list(self.users.create(query, variables))
            for (name, value) in id_list:
                if name in result.keys():
                    result[name].append(value)
                else:
                    result[name] = [value]
            return result

    def get_id(self, interface):

        def _format(name: str):
            name = name.lower()
            if name.startswith("create") or name.startswith("update"):
                name = name[6:]
            if name.endswith("s"):
                name = name[:-1]
            if name.endswith("input"):
                name = name[:-5]
            return name

        def count(_value: dict):
            length = len(_value["value"])
            if _value["num"] + 1 == length:
                _value["num"] = 0
            else:
                _value["num"] += 1

        for key, value in self.id.items():
            # 如果上一层的名字就可以分辨的话，如spareParts,如果不行再向上一层CreateThingInspectionInput分辨
            try:
                if interface.input_name == key.lower():
                    count(value)
                    return value["value"][value["num"]]
                if _format(interface.name) == key.lower():
                    count(value)
                    return value["value"][value["num"]]
                elif _format(interface.parent.name) == key.lower():
                    count(value)
                    return value["value"][value["num"]]
                elif _format(interface.input_name) == key.lower():
                    count(value)
                    return value["value"][value["num"]]
                elif _format(interface.parent.parent.interface) + _format(interface.parent.name) == key.lower():
                    count(value)
                    return value["value"][value["num"]]
            except AttributeError:
                pass

        print("no matchId")
        if self._num > 3:
            self._num = 1

        return self._num
        # raise Exception("no matchId")


@singleton
class UserLoader(object):

    def __init__(self):
        self.users = []
        users = config.get_web_information("users")
        for user_name in users.keys():
            login = users[user_name].get("login")
            interfaces = users[user_name].get("interfaces")
            if interfaces == "all":
                interfaces = interface_info.get_all_interface_name()
            user = {"name": user_name, "client": User(login, interfaces)}
            self.users.append(user)
        self._add_user()

    def _add_user(self):
        for user in self.users:
            interface_info.set_users(user["name"], user["client"].use_interfaces)

    def create(self, query_name, variables):
        for user in self.users:
            if query_name in user["client"].use_interfaces:
                yield from user["client"].send_request(query_name, variables).find_all_id()
                break

    def __getattr__(self, item):
        for user in self.users:
            if user.get("name") == item:
                return user.get("client")


@singleton
class IdMap:
    def __init__(self):
        self.id_map = config.get_web_information("id_map")

    def __call__(self, item):
        return self.id_map.get(item)


class User(GraphqlClient):

    def __init__(self, login, use_interfaces):
        super(User, self).__init__(login=login)
        self.use_interfaces = use_interfaces
