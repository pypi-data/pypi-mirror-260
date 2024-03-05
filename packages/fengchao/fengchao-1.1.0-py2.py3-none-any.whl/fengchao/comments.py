# -*- coding:utf-8 -*-
"""
# File       : comments.py
# Time       ：2024/2/23 13:48
# Author     ：andy
# version    ：python 3.9
"""
from dataclasses import dataclass


@dataclass
class Comments:
    BASE_URL = "http://192.168.1.233:6000"
    LOCAL_URL = "/aigc/local_chat/"
    ONLINE_URL = "/aigc/chat/"
    MODELS_URL = "/aigc/models/"
    PROMPTS_URL = "/aigc/prompts/"
    KGS_URL = "/aigc/kgs"

    RETRY_NUM = 3
    TIMEOUT = 600