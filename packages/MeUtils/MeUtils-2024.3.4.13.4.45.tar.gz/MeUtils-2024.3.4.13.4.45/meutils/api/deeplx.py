#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : deeplx
# @Time         : 2024/3/1 16:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


@lru_cache
def translate(text: str = "Hello, world!", source_lang: str = "auto", target_lang: str = "ZH"):
    """https://fakeopen.org/DeepLX/#%E6%8E%A5%E5%8F%A3%E5%9C%B0%E5%9D%80"""
    url = "https://api.deeplx.org/translate"
    payload = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }

    response = httpx.post(url, json=payload)
    return response.json()


if __name__ == '__main__':
    print(translate())
