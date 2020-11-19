from ..caps.read_yaml import config
from ..tools import singleton
from support.base_test.generate_param.newSchema import base_schema
from ..data_maker import GraphqlClient
import random


@singleton
class ResourceLoader(object):
    """
    id对应格式：
    ('Thing', {'value': ['e081658a-882d-42e4-8419-01abbcc58d9e', 'e181658a-882d-42e4-8419-01abbcc58d9e'], 'num': 0})
    id_map对应格式
    {'thing': 'createThing'}
    users对应格式
    {'name': 'simple_user', 'client': <support.base_test.ResourceLoader.User object at 0x109e4dc18>}
    """

    def __init__(self):
        self.interface = base_schema
        self.users = UserLoader()
        self.id_map = IdMap()
        self.id = {}
        self._num = 0

    def __getattr__(self, item):
        if "user" in item:
            return getattr(self.users, item)
        else:
            return self.interface.find(item)

    def import_id(self, id_map: dict):
        for name, _id in id_map.items():
            self.id[name.lower()] = {"value": _id, "num": 0}

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

    def get_id(self, name):
        if name:
            name = name.lower()
            _id = self.id[name]["value"][self.id[name]["value"]]
            return random.choice(_id)
        else:
            raise KeyError


@singleton
class UserLoader(object):

    def __init__(self):
        self.users = []
        users = config.get_web_information("users")
        for user_name in users.keys():
            login = users[user_name].get("login")
            interfaces = users[user_name].get("interfaces")
            user = {"name": user_name, "client": User(login, interfaces)}
            self.users.append(user)

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


resource = ResourceLoader()
