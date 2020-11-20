# coding=utf-8

import logging
import time
from beeprint import pp
import os


def singleton(cls):
    instances = {}

    # instances变量以什么形式存在呢？
    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class AutoTestLog(object):
    def __init__(self):
        # 创建一个record
        self.record = logging.getLogger("mytest")

        # 置顶日志级别
        self.record.setLevel(logging.DEBUG)
        # print(self.record.handlers)

        # 给日志命名
        now = time.strftime("%Y-%m-%d %H-%M-%S")
        file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/output/log/'
        log_name = file_path + now + '.log'
        # log_name = r'../output/log/' + now + '.log'

        # 将日志写入磁盘
        self.file_handle = logging.FileHandler(log_name, 'a', encoding='utf-8')
        self.file_handle.setLevel(logging.DEBUG)

        # 设置日志格式
        file_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s -%(message)s')
        self.file_handle.setFormatter(file_formatter)

        # 给log添加handle
        self.record.addHandler(self.file_handle)

    def get_log(self):
        return self.record

    # 关闭handle
    def close_handle(self):
        self.record.removeHandler(self.file_handle)
        self.file_handle.close()

    # def __del__(self):
    #     self.close_handle()
    #     print("销毁")


def pformat(strings):
    return pp(strings, output=False)


logger = AutoTestLog().get_log()
if __name__ == '__main__':
    print(os.path.abspath(__file__))
    obj = AutoTestLog()
    # obj.get_log().debug('日志1')
    # obj.close_handle()
