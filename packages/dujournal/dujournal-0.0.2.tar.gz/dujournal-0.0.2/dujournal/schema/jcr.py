# -*- coding: utf-8 -*-
# @time: 2024/3/5 16:11
# @author: Dyz
# @file: jcr.py
# @software: PyCharm
from typing import List

from du_aio_tools.schemas import BaseSchemas
from pydantic import validator


def reset_sn(val: str):
    """校验 sn"""
    if val:
        val = val.upper()
    if '**' in val or 'n/a' in val:
        return ''
    return val.strip()


class EsiHit(BaseSchemas):
    esi_date: str
    abbr: str = None
    abbr2: str = None
    category: str = None


class JcrHit(BaseSchemas):
    ename: str
    abbr: str
    year: int
    issn: str = ''
    eissn: str = ''
    yx: str
    edition: List = []
    zone_rank: List = []
    fq: List = []

    @validator('edition')
    def check_edition(cls, val):
        return list(set(val))

    @validator('issn')
    def check_sn(cls, val):
        return reset_sn(val)

    @validator('eissn')
    def check_en(cls, val):
        return reset_sn(val)

    @validator('yx')
    def check_yx(cls, val):
        if val.upper() == 'N/A':
            return 0
        if '<' in val:
            return val.replace('<', '').strip()
        return val or 0
