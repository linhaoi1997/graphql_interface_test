import functools
from support.tools.log import AutoTestLog

record = AutoTestLog().get_log()


class Decorator(object):

    # 装饰器工具函数
    @staticmethod
    def log_process(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            record('%s 用例开始:' % func.__name__)
            result = func(*args, **kw)
            record('%s 用例结束:' % func.__name__)
            return result

        return wrapper

    # 多装饰器装饰case
    def log_allure_story(self):
        pass


if __name__ == "__main__":
    @Decorator.log_process
    def test():
        print("用例进行")
        return 1


    print(test())
