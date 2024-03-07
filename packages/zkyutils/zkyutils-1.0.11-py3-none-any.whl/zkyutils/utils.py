import os
import json
from zkyutils.logger import log


@log.log_decorator('读取json')
def read_json(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


@log.log_decorator('写入json')
def write_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@log.log_decorator('批量获取用户输入')
def get_input_list(msg):
    input_list = []
    data = input(msg)
    while data != '':
        input_list.append(data)
        data = input('')
    return input_list
