# -*- coding: utf-8 -*-
# @time: 2024/2/26 11:13
# @author: Dyz
# @file: zky.py
# @software: PyCharm
from typing import Union

from du_aio_tools.schemas import BaseSchemas


class ZkyWarnHit(BaseSchemas):
    year: int  # 年分
    ename: str  # 刊名
    issn: Union[str, None] = None  # issn
    level: str  # 预警级别/预警原因


class ZkyHit(BaseSchemas):
    year: int
    ename: str
    abbr: str
    issn: str = None
    zky_big: list = None
    zky_small: list = None
    data: dict = None
