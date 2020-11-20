from Apis.Employees.me import Me
from support import BaseTestCase, run


class TestMe(BaseTestCase):
    me = Me()

    def test_me(self, resource):
        result = self.me.return_my_id()
        self.assertCorrect(result)


if __name__ == '__main__':
    run(__file__)
