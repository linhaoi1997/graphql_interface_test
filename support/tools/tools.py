import random
import time
import os
import shutil
import allure
from copy import deepcopy
from support.caps.read_yaml import config


def create_num_string(num, default=0):
    result = ''
    for i in range(num):
        if default == 0:
            result += random.choice('abcdefghijklmnopqrstuvwxyz')
        elif default == 1:
            result += random.choice('abcdefghijklmnopqrstuvwxyz0123456789')
        elif default == 2:
            result += random.choice('abcdefghijklmnopqrstuvwxyz0123456789_')
        elif default == 3:
            result += random.choice('123456789')
    return result


def create_timestamp(delay=0):
    return int(time.time() * 1000) + delay * 60 * 1000


def get_all_deepest_dict_gen(test_dict, sign=''):
    for i in test_dict.keys():
        if type(test_dict[i]) == dict:
            for j in get_all_deepest_dict_gen(test_dict[i], i + "_"):
                yield j
        else:
            yield {sign + i: test_dict[i]}


def convert_list_to_dict(lambel, test_dict, query_name):
    query_str = "$.."
    if query_name:
        query_str = query_str + query_name + '.'
    result = {}

    for i in test_dict:
        for j in i.keys():
            if isinstance(i[j], list):
                for num in range(len(i[j])):
                    se_lambel = lambel + "[%s]." % test_dict.index(i) + j
                    result.update(convert_list_to_dict(se_lambel, i[j], query_name))
            elif isinstance(i[j], dict):
                for key in i[j].keys():
                    se_lambel = lambel + "[*]." + j + "." + key
                    if query_str + se_lambel in result.keys():
                        result[query_str + se_lambel].append(deepcopy(i[j][key]))
                    else:
                        result[query_str + se_lambel] = deepcopy([i[j][key]])
            else:
                if query_str + lambel + "[*]." + j in result.keys():
                    result[query_str + lambel + "[*]." + j].append(deepcopy(i[j]))
                else:
                    result[query_str + lambel + "[*]." + j] = deepcopy([i[j]])
    return result


def get_all_deepest_dict(test_dict, query_name=''):
    result = {}
    for s in get_all_deepest_dict_gen(test_dict):
        result.update(s)
    new_result = {}
    for i in result.keys():
        if "_" in i:
            first_name, last_name = i.split("_")
            name = first_name + "." + last_name
        else:
            name = i
        temp = result[i]
        if type(result[i]) == list and result[i]:
            new_result.update(convert_list_to_dict(i, temp, query_name))
        else:
            new_result.update({"$.." + name: temp})

    return new_result


def format_number(num_list: list):
    if num_list == [None]:
        return []
    if type(num_list) == list:
        for i in range(len(num_list)):
            try:
                num_list[i] = int(num_list[i])
            except:
                pass
        try:
            num_list.sort()
        except:
            pass
        return num_list


def go_allure(isClear=False):
    allure_path = config.get_file_path("allure")
    pro_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    xml_path = pro_path + "/output/report/xml/"
    html_path = pro_path + "/output/report/html/"
    print(xml_path)
    command = allure_path + "allure generate " + xml_path + " -o " + html_path + " --clean"
    os.popen(command)
    if isClear:
        shutil.rmtree(xml_path)
        os.mkdir(xml_path)
        log_path = pro_path + "/output/log/"
        shutil.rmtree(log_path)
        os.mkdir(log_path)


def record(body, title=""):
    allure.attach(str(body), str(title), allure.attachment_type.TEXT)


if __name__ == "__main__":
    # test = {
    #     'input': {'code': 'fdmtzggqpv', 'name': 'test_003', 'type': 'PRODUCTION', 'model': 'TEST', 'concat': 'linhao',
    #               'phone': '157', 'desc': '这是接口测试的设备', 'images': [{'id': 1}, {'id': 2}], 'spareParts': None,
    #               'attachments': [{'id': 3}, {'id': 4}], 'location': 'hangzhou', 'manufacturer': 'manufacturer_002',
    #               'distributor': 'manufacturer_002', 'purchasedAt': 1589856285676, 'activatedAt': 1589856285676,
    #               'purchasedPrice': 1000, 'yearsOfUse': 100, 'depreciationRate': 0.5}}
    # print(get_all_deepest_dict(test))
    pass
