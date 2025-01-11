import json
import re

import requests
import hashlib
import time
import random

from sympy.physics.mechanics import body


def getParams():
    # 生成随机数和时间戳
    n = random.randint(1, 10)  # 生成 1 到 10 之间的随机整数
    i = int(time.time() * 1000)  # 获取当前时间戳（毫秒）
    s = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    f = "&key=A013F70DB97834C0A5492378BD76C53A"
    # 构造待签名的字符串
    c = (
        f"method=GET&timeStamp={i}"
        f"&User-Agent={s}"
        f"&index={n}"
        f"&channelId=40011"
        f"&sVersion=1"
    )
    # 计算 MD5 哈希值
    md5_hash = hashlib.md5((c + f).encode("utf-8")).hexdigest()
    # 构造参数字典
    params = {
        "timeStamp": i,
        "index": n,
        "signKey": md5_hash,
        "sVersion": 1,
        "channelId": 40011,
        'webdriver': 'false',
        "WuKongReady": "h5",
    }
    return params

def get_mygsig(url, params, headers, body):
    info = params.copy()
    info["path"] = url.replace("https://www.maoyan.com", "")
    # 将参数转换为字符串并排序
    sorted_params = sorted(info.items(), key=lambda x: x[0].lower())
    str_to_hash = "_".join([str(value) for key, value in sorted_params])

    prefix = "581409236"
    time_stamp = int(time.time() * 1000)
    ms1 = f"{prefix}#{str_to_hash}${time_stamp}"

    # 计算 MD5 哈希值
    hash_hex = hashlib.md5(ms1.encode("utf-8")).hexdigest()

    mygsig = {
        "m1": "0.0.1",
        "m2": "0",
        "ms1": hash_hex,
        "ts": time_stamp,
    }
    return json.dumps(mygsig)

def getHeaders(url,params):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': '_ga=GA1.1.427435205.1732029469; _lxsdk_cuid=19345005032c8-0452f97f12a0d1-26011951-1fa400-19345005032c8; uuid_n_v=v1; uuid=2D3DE750C96B11EF8BF5E789F57BC8028090C83F046C49CF99937114F4A20123; _lxsdk=2D3DE750C96B11EF8BF5E789F57BC8028090C83F046C49CF99937114F4A20123; _csrf=cb9ade84dbd3e02ad7bad93f4c3f6e0cf8e0dc2e9c11f8e63fd50ab1d115e32b; Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1736512484,1736522213,1736522432,1736522892; HMACCOUNT=0AF1B23D10885BE0; __mta=242479805.1732029470408.1736524542519.1736524586072.55; Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1736547661; _lxsdk_s=19452469ec0-c15-637-a6d%7C%7C8; _ga_WN80P4PSY7=GS1.1.1736538452.59.1.1736548385.0.0.0',
        'Referer':re.sub('/ajax', '', url),
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'mygsig': '{"m1":"0.0.1","m2":0,"ms1":"bde9477b566800dd31dc75523e29fbed","ts":1736548401225}',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    mygsig = get_mygsig(url, params, headers, None)
    headers["mygsig"] = mygsig
    return headers

def getCookies():
    cookies = {
        '_ga': 'GA1.1.427435205.1732029469',
        '_lxsdk_cuid': '19345005032c8-0452f97f12a0d1-26011951-1fa400-19345005032c8',
        'uuid_n_v': 'v1',
        'uuid': '2D3DE750C96B11EF8BF5E789F57BC8028090C83F046C49CF99937114F4A20123',
        '_lxsdk': '2D3DE750C96B11EF8BF5E789F57BC8028090C83F046C49CF99937114F4A20123',
        '_csrf': 'cb9ade84dbd3e02ad7bad93f4c3f6e0cf8e0dc2e9c11f8e63fd50ab1d115e32b',
        'Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533': '1736512484,1736522213,1736522432,1736522892',
        'HMACCOUNT': '0AF1B23D10885BE0',
        '__mta': '242479805.1732029470408.1736524542519.1736524586072.55',
        'Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533': '1736547661',
        '_lxsdk_s': '19452469ec0-c15-637-a6d%7C%7C8',
        '_ga_WN80P4PSY7': 'GS1.1.1736538452.59.1.1736548385.0.0.0',
    }
    return cookies

def  main():
    url = "https://www.maoyan.com/ajax/films/1519877"
    params = getParams()
    headers = getHeaders(url, params)
    cookies = getCookies()
    print(params)
    print(headers)
    res = requests.get(url, headers=headers, cookies=cookies, params=params)
    print(res.text)


if __name__ == '__main__':
    main()