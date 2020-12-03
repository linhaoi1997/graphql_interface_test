from faker import Faker
from support.tools.tools import create_num_string
from support.tools.log import logger
from faker.providers import BaseProvider


class MyProvider(BaseProvider):
    fake = Faker(['zh_CN', 'en_US', 'ja_JP'])

    def code(self):
        return self.fake.currency_code() + str(self.fake.random_int())

    def model(self):
        return self.fake.word() + self.fake.gou()


class MyFaker(object):

    def __init__(self):
        self.fake = Faker()
        self.fake.add_provider(MyProvider)
        self.fake_map = {
            "contact": "name",
            "phone": "phone_number",
            "desc": "sentence",
            "location": "address",
            "manufacturer": "company",
            "distributor": "company",
        }

    def create_string(self, param, **identity):
        name = param.param.real_name
        if getattr(self, name.lower()):
            return getattr(self, name.lower())
        if identity.get("is_random", False):
            str_len = identity.get("string_len", 5)
            return name + "_" + create_num_string(str_len, 1)
        elif identity.get("num"):
            return name + "_" + str(identity.get("num"))
        else:
            return name

    def __getattr__(self, item):
        if item == "password":
            return self.fake.password(special_chars=False)
        try:
            return getattr(self.fake, item)()
        except AttributeError:
            try:
                return getattr(self.fake, self.fake_map[item])()
            except KeyError:
                logger.debug("fake_map 不存在 %s" % item)
            except AttributeError:
                logger.debug("fake_map %s 的对应不对")
        return None


fake = MyFaker()
