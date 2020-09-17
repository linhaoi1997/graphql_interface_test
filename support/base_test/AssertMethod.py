import jsonpath
from ..tools.log import logger, pformat
from ..tools import get_all_deepest_dict, format_number, find_return_type
from ..data_maker.VariableMaker import TypeSearcher
import json


class AssertMethod(object):
    # 校验相关
    # 校验json中某个值相等
    def assertJsonResponseEqual(self, json_path, json_data, value):
        result = jsonpath.jsonpath(json_data, json_path)
        result = [None] if not result else result
        if "[" not in json_path:
            result = result[0]
        logger.debug(
            "\njsonpath : '%s'\nget\n'%s'\nfrom\nresult" % (json_path, pformat(result)))
        logger.debug("except %s" % value)
        """Jsonpath取到的值与value一致"""
        if not result and not value:
            pass
        else:
            self.assertEqual(value, result)

    # 校验json含有某个key,并且有值
    def assertJsonResponseIn(self, json_path, json_data):
        result = jsonpath.jsonpath(json_data, json_path)
        logger.debug("\njsonpath : '%s'\nget\n'%s'\nfrom\nresult" % (json_path, pformat(result)))
        """jsonpath能在json中取到值"""
        assert result
        assert result[0]

    # 校验json某个路径下包含某个字符串
    def assertJsonMessageContain(self, json_path, json_data, value):
        flag = False
        result = jsonpath.jsonpath(json_data, json_path)
        logger.debug("\njsonpath : '%s'\nget\n'%s'\nfrom\nresult" % (json_path, pformat(result)))
        logger.debug("except %s" % value)
        assert result
        for i in result:
            if value in i.lower():
                flag = True
        assert flag

    # 校验json返回多个值计数是否是想要的数字（主要针对返回多个结果的计数校验）
    def assertJsonCountEqual(self, json_path, json_data, num):
        result = jsonpath.jsonpath(json_data, json_path)
        logger.debug("\njsonpath : '%s'\nget\n'%s'\nfrom\nresult" % (json_path, pformat(result)))
        if not result:
            count = 0
        else:
            count = len(result)
        logger.debug("get numbers %s" % count)
        logger.debug("except %s" % num)
        assert count == num

    # 校验json某个value不为none
    def assertJsonNotNone(self, json_path, json_data):
        result = jsonpath.jsonpath(json_data, json_path)
        logger.debug("\njsonpath : '%s'\nget\n'%s'\nfrom\nresult" % (json_path, pformat(result)))
        logger.debug("except something")
        assert result and result[0]

    # 检验每一个输入参数都和返回的json一样
    def assertEveryParam(self, variables, result):
        if variables.get("input"):
            variables = variables["input"]
        if variables.get("addition"):
            addition = json.loads(variables.pop("addition"))
            addition_result = json.loads(jsonpath.jsonpath(result, "$..addition")[0])
            for i in addition_result:
                for j in addition:
                    if i["key"] == j["key"]:
                        self.assertEqual(i["value"], j["value"])
                        break
                else:
                    raise AssertionError("key缺失")
        deepest_dict = get_all_deepest_dict(variables, self.query_name)
        for i in deepest_dict.keys():
            self.assertJsonResponseEqual(i, result, deepest_dict[i])

    def assertEqual(self, value, result):
        if type(value) == str and value.isdigit():
            if type(result) in (str, int):
                assert int(value) == int(result)
        elif type(value) in (int, float):
            if type(result) in (str, int, float):
                assert int(value) == int(result)
            else:
                assert None
        elif type(value) == list:
            assert format_number(value) == format_number(result)
        else:
            assert value == result

    def assertDict(self, result, value):
        pass

    # 确认返回type都有值，适用于schema中type的列表都会返回值的情形
    def assertReturnType(self, result, filter_list=[]):
        return_type = find_return_type(self.query_name)
        if "ID" not in return_type:
            assert_list = TypeSearcher(return_type).msg
            for i in assert_list:
                if i not in filter_list:
                    json_path = "$.data." + self.query_name + "." + i
                    self.assertJsonResponseIn(json_path, result)
        else:
            json_path = "$.data" + self.query_name
            self.assertJsonResponseIn(json_path, result)

    # 验证删除/查询接口返回值ids是预期值
    def assertIds(self, variables, result):
        self.assertCorrect(result)
        self.assertJsonResponseEqual("$.." + self.query_name + "[*]", result, variables["input"]["ids"])

    def assertIds_query(self, variables, result):
        self.assertCorrect(result)
        self.assertJsonResponseEqual("$.." + self.query_name + ".data[*].id", result, variables)

    # 验证创建/更新接口返回值是预期值
    def assertForm(self, variables, result):
        self.assertCorrect(result)
        self.assertEveryParam(variables, result)

    # 验证预计返回正确的结果
    def assertCorrect(self, result):
        self.assertJsonResponseEqual("$..errors", result, None)

    # 验证预计返回错误的结果
    def assertError(self, result):
        self.assertJsonResponseIn("$..errors", result)

    # 下面是针对每种类型接口通用校验
    # 验证query接口返回值没有问题
    def assertQuery(self, _, result):
        self.assertCorrect(result)
        self.assertEveryParam(_, result)

    # 验证querys接口返回值没有问题
    def assertQuerys(self, _ids, result):
        self.assertCorrect(result)
        self.assertIds_query(_ids, result)

    # 验证导出接口返回值是预期值
    def assertExport(self, result):
        self.assertCorrect(result)
        self.assertJsonResponseIn("$..data", result)

    # 验证创建接口返回值是预期值
    def assertCreate(self, variables, result):
        self.assertForm(variables, result)

    # 验证更新接口返回值是预期值
    def assertUpdate(self, variables, result):
        self.assertForm(variables, result)

    # 验证删除接口返回值是预期值
    def assertDelete(self, variables, result):
        self.assertIds(variables, result)


if __name__ == "__main__":
    test = AssertMethod()
    test.assertEqual(None, 100)
