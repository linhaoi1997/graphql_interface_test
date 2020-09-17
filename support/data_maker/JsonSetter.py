class JsonSetter(object):

    def __init__(self, expr):
        self.expr_list = [Field(i) for i in expr.split('.')]
        self.length = len(self.expr_list)

    def set(self, test_json: dict, value, num=0):
        expr = self.expr_list[num]
        if expr.type == "list" and isinstance(test_json[expr.name], list):
            if expr.value != "*":
                self.set(test_json[expr.name][int(expr.value)], value, num + 1)
            else:
                for i in test_json[expr.name]:
                    self.set(i, value, num + 1)
        else:
            if num == self.length - 1:
                test_json[expr.name] = value
            else:
                self.set(test_json[expr.name], value, num + 1)


class Field(object):

    def __init__(self, single_expr):
        '''
        记录单个路径的
            类型：type
            名称：name
            如果是列表的话有具体的值： value 可以是 * 或者数字
        '''
        self.type, self.name, self.value = Field._analysis(single_expr)
        print(self.type, self.name, self.value)

    @staticmethod
    def _analysis(single_expr: str):
        if single_expr.endswith("]"):
            name, msg = single_expr.split("[")
            return "list", name, msg[:-1]
        else:
            return "str", single_expr, None


if __name__ == '__main__':
    d = {
        "error_code": {"code": 1000},
        "stu_info": [
            {
                "id": 314,
                "name": "矿泉水",
                "sex": "男",
                "age": 18,
                "addr": "北京市昌平区",
                "grade": "摩羯座",
                "phone": "18317155663",
                "gold": 100,
                "cars": [
                    {"car1": "bmw"},
                    {"car2": "ben-z"},
                ]
            },
            {
                "id": 315,
                "name": "矿泉水",
                "sex": "男",
                "age": 18,
                "addr": "北京市昌平区",
                "grade": "摩羯座",
                "phone": "18317155663",
                "gold": 100,
                "cars": [
                    {"car1": "bmw"},
                    {"car2": "ben-z"},
                ]
            }
        ]

    }
    from beeprint import pp

    test = JsonSetter("stu_info[*].id")
    # test = JsonSetter("error_code.code")
    test.set(d, 100)
    pp(d)
