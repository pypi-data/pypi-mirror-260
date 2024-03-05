from . import pack
from . import rsa
from . import http
import json
import requests


# 读取JSON文件
def read_json(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    # 打印JSON数据
    print(type(data))
    print(data)
    return data


def read_json_online(file_url: str):
    # 定义文件的 URL
    # file_url = "https://shouqianba-vip.oss-cn-hangzhou.aliyuncs.com/cis/t/2024-01/cis-operation-backend/file/1706563139894.json"
    try:
        # 发起 GET 请求获取文件内容
        response = requests.get(file_url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 读取 JSON 数据
            json_text = response.text
            # 打印 JSON 数据或进行其他处理
            # print(json_text)
            return json_text
        else:
            print("Failed to retrieve file. Status code:", response.status_code)
    except Exception as e:
        print("Error:", e)