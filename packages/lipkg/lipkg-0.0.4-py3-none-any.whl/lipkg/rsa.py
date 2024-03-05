import json
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def signer(data_dict: dict, key_path = ""):
    """
    加签
    :param data_dict: 待签名dict对象
    :param key_path: 密钥路径
    :return: 签名(str)
    """
    if key_path == "":
        print("请输入密钥路径")
        return
    with open(key_path, mode='rb') as f:
        rsa_private_key = RSA.import_key(f.read())
    secret_key_obj = PKCS1_v1_5.new(rsa_private_key)
    request_hash = SHA256.new(json.dumps(data_dict, separators=(',', ':'), ensure_ascii=False).encode('utf-8'))
    return base64.b64encode(secret_key_obj.sign(request_hash)).decode('utf-8')


def verifier(data_dict: dict, signature: str, key_path: str) -> bool:
    """
    验签
    :param data_dict: 待验签dict对象
    :param signature: 签名
    :param key_path: 公钥路径
    :return: bool
    """
    with open(key_path, mode='rb') as f:
        rsa_public_key = RSA.import_key(f.read())
    secret_key_obj = PKCS1_v1_5.new(rsa_public_key)
    request_hash = SHA256.new(json.dumps(data_dict, separators=(',', ':'), ensure_ascii=False).encode('utf-8'))
    signature = base64.b64decode(signature)
    return secret_key_obj.verify(request_hash, signature)


def signer_by_str(data_dict: dict, rsa_private_key_str: str):
    """
    加签
    :param data_dict: 待签名dict对象
    :param rsa_private_key_str: RSA私钥字符串
    :return: 签名(str)
    """
    if not rsa_private_key_str:
        print("请输入有效的RSA私钥字符串")
        return

    rsa_private_key = RSA.import_key(rsa_private_key_str)
    secret_key_obj = PKCS1_v1_5.new(rsa_private_key)
    request_hash = SHA256.new(json.dumps(data_dict, separators=(',', ':'), ensure_ascii=False).encode('utf-8'))
    return base64.b64encode(secret_key_obj.sign(request_hash)).decode('utf-8')
#
# # 使用示例
# data = {"key1": "value1", "key2": "value2"}
# private_key_str = '-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAnv4/EglSYJLqt1RdtExQorlNc9a3flV5XxdHZGgSscpJfjMWlULHRkHpXTzFg7exkxAGk4HGwGmsU9UtbFErc/UzZdNo4LrYsmfueYhK+OuJeGU1VQUJNCpQ36gG/UouqFsNhJ79tGxI7YGVqYIsm1ur2OuEiLS7Y+xuXrQhSeDOKhjgDacfVBDdn0LgxU0j2xkCotBffN3mkwXY680RK+T1s+C+DO41OkkEoBLHvZooYfb8FrfnfQn37vqJ1MTwL1teCXupFt1gO0tL8sk7AFHHsrIKrzimUIaBLPi3oPQ0Q+1BsIp7k3NwPakmCBgG/Fdp29K9D+V7IJlExJlWZwIDAQABAoIBAH9k+ORa08bN8YQz9WEiRPodwBGxWhXAJyAqZuns+g27KGgWR2IRv9prtbEfoKOJ7J8JmDtZIQfLpGkHxv2jjE29ixFr8/0ducQ5wrtembQaBmyRq8oT3uwNe/+5guAxMHF1g79gJakLmuOzkVfhFhzltyx4ihl/tya5qzX23zVxxcHUO3oByJgm2nlYH1AWN4FDwdGJ8n93trn690L1eUOezVAseWL2Ij+844+f7hZO+nBgwvQpB9C7WdrmDMjLceYiE5kITtvReyGOxJjsBE2EvWlu7HekSDFOjyf0HFHs+IkyC6jaheno2cdmlkh/M/n4BUlW5+gKOXVC6wqYZQECgYEA5Xcwou5a7Dk+MP4N8b+7DPn3o/HuKkkM6/uRr9g6Bkfxqr6w3fwYkf1bWLUg6SXt0jzhGBMUcnnlpVobmmtgIguPVC8FSVpSap304ki+IKlMBaX4xTD+vuSh30WjGMYmzUgfRXzgQIF3Bfg+CCExFbEHNUwk5igeWRqY3nEYeoUCgYEAsWDhE2ZyuDRVAGbtXUaEysqwaLovuKqj8SUseKXXs7f/EQICbpOlGHH5MxxhbCJfqFx9Yc5iHJbcWpXOrGoOP++YRrfZjZTCskjkWE97IEyup8Wutmgl772HB1n69le3Cv14FQf0QolpcV44lVOH9EqhfHjD6GH+0YdYYjRJPvsCgYEAvYXJLPkzLaJF5I8hE0ephZk72TPr4w781jes55Dus9teFglz6ZTa8lFQzh6j9Q03tQpFW+3+WGKnsv+OhuciulvT4NMJScGJCrg112P/bNiHiq6/npbOAPqzW8aXY9HdoHVuJqVyTrTfipWzHmHTubfCXVnrrBD8p9mY4ziD4EUCgYBiB+Tcz/X/EA0aV8g/kMW7PiIY/y14pfZNQ/o8A4we60WwpKerbTYFOJg9QyYkmSq85cD12RYoLshB2CGM8GBHvacvDlTSBrFDzz1EAUlPJJIybvKMJSsyQFDsIzKsCvZCwKspFGhOjZsU6Lnk7XFp9gUhwaykNeSa8G5MeBEzGQKBgDPv3JTAbYejXJRX+SyBnPCV3eO4CNjG4JvGtOyPWlcOxa6Tj8sifWGcB90F2KEPTJ92pXKHlPAVbPRVtvvDNwydG7rL5MZhfQALfuahbBY95oth1uU9lVr/tBJRU+lHq+5NtFpi+GxR3NXajNL+c+P1NKbyKQgU/Zb9NOMiWyG8\n-----END RSA PRIVATE KEY-----'
# signature = signer(data, private_key_str)
# print("Signature:", signature)


def sign(data_dict: dict, key: str = None, key_path: str = None):
    if key is None and key_path is None:
        raise ValueError("Please provide either a key or a key path.")
    if key:
        rsa_private_key = RSA.import_key(key)
    else:
        with open(key_path, mode='rb') as f:
            rsa_private_key = RSA.import_key(f.read())
    secret_key_obj = PKCS1_v1_5.new(rsa_private_key)
    request_hash = SHA256.new(json.dumps(data_dict, separators=(',', ':'), ensure_ascii=False).encode('utf-8'))
    return base64.b64encode(secret_key_obj.sign(request_hash)).decode('utf-8')