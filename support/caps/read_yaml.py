# coding:utf-8
import yaml
import os


class Config(object):
    def __init__(self):
        self.cur_path = os.path.dirname(os.path.realpath(__file__))
        self.path_config = self.read_yaml("path.yaml")
        self.web_config = self.read_yaml("web_information.yaml")

    def read_yaml(self, file_name):
        yaml_path = os.path.join(self.cur_path, file_name)
        with open(yaml_path, 'r', encoding='utf-8') as f:
            cfg = f.read()
        d = yaml.safe_load(cfg)
        return d

    def get_file_path(self, name):
        return self.path_config.get(name)

    def get_web_information(self, *name):
        if not name:
            return self.web_config
        elif len(name) == 1:
            return self.web_config.get(name[0])
        else:
            return [self.web_config.get(i) for i in name]

    def get_account(self, name):
        info = self.get_web_information("users")
        return info.get(name).get("login")


config = Config()

if __name__ == "__main__":
    assert config.get_file_path("allure") == "/Users/linhao/Desktop/linhao/project/allure-2.13.1/bin/"
    assert config.get_web_information('db') == ['postgres', 'postgres', '192.168.1.175', '9990']
    assert config.get_account("simple_user") == {'account': 'admin_jia', 'passpord': '123456'}
