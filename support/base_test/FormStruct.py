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
        "title": "多行文字",
        "deletable": True,
        "fieldRatio": 50,
        "isSingleLine": True
    }, {
        "type": "CONTACT",
        "title": "联系方式",
        "deletable": True,
        "fieldRatio": 50,
        "isSingleLine": True
    }, {
        "type": "DATETIME",
        "title": "日期",
        "deletable": True,
        "fieldRatio": 50
    }, {
        "type": "NUMBER",
        "title": "数字",
        "deletable": True,
        "fieldRatio": 50
    }, {
        "type": "SINGLE_SELECTION",
        "title": "单选",
        "deletable": True,
        "fieldRatio": 50,
        "candidates": ["1", "2", "3"]
    }, {
        "type": "MULTI_SELECTION",
        "title": "多选",
        "deletable": True,
        "fieldRatio": 50,
        "candidates": ["1", "2", "3"]
    }
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
