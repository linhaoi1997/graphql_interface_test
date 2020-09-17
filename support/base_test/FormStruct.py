# from .ResourceLoader import ResourceLoader
from support.base_test.ResourceLoader import ResourceLoader
from support.base_test.form import form_list
from beeprint import pp

resource = ResourceLoader()
user = resource.simple_user


def recover_form_struct():
    query_name = "updateFormStruct"
    for variable in form_list:
        _result = user.send_request(query_name, variable).find_result("$..errors")[0]
        if _result:
            raise Exception("没刷新成功，看一眼")


def test_form_struct(test=True):
    if test:
        add = addition_test
    else:
        add = addition
    query_name = "updateFormStruct"
    for variable in form_list:
        variable["customFields"].extend(add)

        _result = user.send_request(query_name, variable).find_result("$..errors")[0]
        if _result:
            print(_result)
            raise Exception("没刷新成功，看一眼")


addition_test = [
    {
        "fieldRatio": 50,
        "isSingleLine": True,
        "deletable": True,
        "title": "单行文字",
        "type": "TEXT",
        "hidden": False
    }
]
addition = [
    {
        "type": "TEXT",
        "title": "单行文字",
        "deletable": True,
        "fieldRatio": 50,
        "isSingleLine": True,
        "hidden": False
    }, {
        "type": "TEXT",
        "title": "多行文字",
        "deletable": True,
        "fieldRatio": 50,
        "isSingleLine": True,
        "hidden": False
    }, {
        "type": "CONTACT",
        "title": "联系方式",
        "deletable": True,
        "fieldRatio": 50,
        "isSingleLine": True,
        "hidden": False
    }, {
        "type": "DATETIME",
        "title": "自定义默认日期",
        "deletable": True,
        "fieldRatio": 50,
        "defaultDatetime": -1,
        "hidden": False
    }, {
        "type": "DATETIME",
        "title": "当前时间默认日期",
        "deletable": True,
        "fieldRatio": 50,
        "defaultDatetime": -1,
        "hidden": False
    }, {
        "type": "DATETIME",
        "title": "普通的日期字段",
        "deletable": True,
        "fieldRatio": 50,
        "hidden": False
    }, {
        "type": "DESCRIPTION",
        "title": "描述文字",
        "deletable": True,
        "fieldRatio": 100,
        "hidden": False
    }, {
        "type": "SINGLE_SELECTION",
        "title": "下拉单选",
        "deletable": True,
        "fieldRatio": 50,
        "candidates": ["1", "2", "3"],
        "hidden": False
    }, {
        "type": "MULTI_SELECTION",
        "title": "下拉多选",
        "deletable": True,
        "fieldRatio": 50,
        "candidates": ["1", "2", "3", "4", "5"],
        "hidden": False
    }, {
        "type": "NUMBER",
        "title": "普通数字-限制小数3",
        "deletable": True,
        "fieldRatio": 25,
        "hidden": False
    }, {
        "type": "NUMBER",
        "title": "普通数字-不限小数位数",
        "deletable": True,
        "fieldRatio": 25,
        "defaultNumber": 2,
        "hidden": False
    }, {
        "type": "NUMBER",
        "title": "普通数字",
        "deletable": True,
        "fieldRatio": 25,
        "defaultNumber": 2,
        "hidden": False
    }, {
        "type": "CONTACT",
        "title": "联系方式-测试必填项/默认内容",
        "deletable": True,
        "required": True,
        "fieldRatio": 50,
        "defaultContact": "111111",
        "hidden": False
    }, {
        "type": "TEXT",
        "title": "文字-限字数2-100",
        "deletable": True,
        "fieldRatio": 25,
        "isSingleLine": True,
        "wordCountLimit": {
            "min": 2,
            "max": 100
        },
        "hidden": False
    },
    # {
    #     "type": "ATTACHMENT",
    #     "title": "测试附件",
    #     "deletable": True,
    #     "fieldRatio": 50,
    #     "hidden": False
    # }, {
    #     "type": "IMAGE",
    #     "title": "测试图片",
    #     "deletable": True,
    #     "fieldRatio": 50,
    #     "hidden": False
    # }
]

if __name__ == '__main__':
    variables = {
        "isDraft": False,
        "name": "things"
    }
    all_forms = ['spare_part_outbounds', 'spare_part_receipts', 'spare_parts', 'thing_inspection_rules',
                 'thing_inspections', 'thing_inspections_feedback', 'thing_maintenance', 'thing_maintenance_feedback',
                 'thing_maintenance_rules', 'thing_repairs', 'thing_repairs_feedback', 'things']
    with open("./form.py", "w") as f:
        for i in all_forms:
            variables["name"] = i
            result = user.send_request("formStruct", variables, has_typename=False).result
            f.write(i + "=")
            result = result["data"]["formStruct"]
            result.pop("displayName")
            result["isPublish"] = True
            f.write(str(result))
            f.write("\n")
        f.write("form_list = " + str(all_forms).replace("'", ''))
    # recover_form_struct()
