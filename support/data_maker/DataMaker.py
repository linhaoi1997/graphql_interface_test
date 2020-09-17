from beeprint import pp
from ..data_maker.InputSearcher import InputSearcher


# 由于graphql接口中部分参数复杂，这里写一个工具类把各个接口的复杂variables制作出来
class DataMaker(object):

    @classmethod
    def make_data(cls, input_name, **kwargs):
        result = []
        # 不把所有为空的项都剔除
        is_not_pop_none = kwargs.pop("is_not_pop_none", True)
        # 把所有为空的项都改成none
        is_change_none = kwargs.pop("is_change_none", True)

        input_searcher = InputSearcher(input_name)
        num = cls.get_deepest_dict(kwargs)
        for i in range(num):
            tmp = {}
            for key in kwargs.keys():
                # print(key)
                tmp[key] = kwargs[key][i]
            tmp_var = cls.make_single_data(input_searcher, **tmp)
            # print(tmp_var)
            if is_change_none:
                format_foreign_items(tmp_var)
            if not is_not_pop_none:
                pop_none(tmp_var)
            result.append({"input": tmp_var})
        return result

    @classmethod
    def make_single_data(cls, input_searcher, var_name="input", **kwargs):

        variables = {}
        is_nothing_pop = kwargs.get("is_nothing_pop", False)
        for i in input_searcher:
            # i为Field类，var_name为变量名称
            if "input" in i.identity:
                get_value = cls.make_single_data(i.input_searcher, i.var_name, **kwargs)
                if "list" in i.identity and get_value:
                    # list要转换格式
                    variables[i.var_name] = cls.convert_dict(get_value)
                else:
                    variables[i.var_name] = get_value
            else:
                tmp_name = i.var_name
                if i.var_name in ("id", "reason", "name"):
                    if var_name != "input":
                        tmp_name = var_name + "_" + i.var_name
                variables[i.var_name] = kwargs[tmp_name]
        return variables

    @classmethod
    def make_simple_data(cls, **kwargs):
        variables = []
        var_len = cls.get_deepest_dict(kwargs)
        for i in range(var_len):
            variable = {}
            for name, value in kwargs.items():
                if "_" not in name:
                    print(variable, value)
                    variable[name] = value[i]
                else:
                    first_name, last_name = name.split("_")
                    variable[first_name] = {last_name: value[i]}
            variables.append({"input": variable})
        return variables

    @classmethod
    def get_deepest_dict(cls, kwargs: dict):
        num = 0
        for i in kwargs.keys():
            if kwargs[i]:
                if len(kwargs[i]) > num:
                    num = len(kwargs[i])
        return num

    @classmethod
    def convert_dict(cls, origin_list):
        result = []
        num = cls.get_deepest_dict(origin_list)
        for i in range(num):
            tmp = {}
            for key in origin_list.keys():
                tmp[key] = origin_list[key][i]
            result.append(tmp)
        return result

    @classmethod
    def assert_none(cls, test_dict: dict):
        for key in test_dict.keys():
            if test_dict[key]:
                return test_dict
            else:
                return None


def traverse_dict(test_dict):
    for i in list(test_dict.keys()):
        if type(test_dict[i]) == dict:
            yield from traverse_dict(test_dict[i])
        elif type(test_dict[i]) == list:
            for j in test_dict[i]:
                yield from traverse_dict(j)
        else:
            yield i, test_dict


def format_foreign_items(temp):
    for i, test_dict in traverse_dict(temp):
        if test_dict[i] == "":
            test_dict[i] = None


def format_list(label_list):
    return [{"id": j} for j in label_list if label_list] or None


def pop_none(var: dict):
    for i, test_dict in traverse_dict(var):
        if test_dict[i] is None:
            test_dict.pop(i)
    for i in list(var.keys()):
        if not var[i]:
            var.pop(i)


if __name__ == "__main__":
    test_variables = {
        "name": [1, 1],
        "desc": [1, 1],
        "type": [1, 1],
        "model": [1, 1],
        "manufacturer": [1, 1],
        "distributor": [1, 1],
        "images_id": [[1, 2], [1]],
        "attachments_id": [[1], [1]],
        "things_id": [[1], [1]],
        "id": [1, 1],
    }
    test_searcher = InputSearcher("CreateSparePartInput")
    test_right_data = DataMaker.make_data(test_searcher, **test_variables)
    pp(test_right_data)
    # test_list = {
    #     'id': [1, 2, 3],
    # }
    # s = DataMaker.convert_dict(test_list)
    # print(s)
