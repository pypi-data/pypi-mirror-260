# -*- coding: utf-8 -*-
# @time: 2024/3/7 10:02
# @author: Dyz
# @file: sjr.py
# @software: PyCharm
from typing import Union, List

import requests
from du_aio_tools.schemas import BaseSchemas
from parsel import Selector
from pydantic import validator

SJR_QUERY = 'https://www.scimagojr.com/journalsearch.php'


class SjrRow(BaseSchemas):
    year: int
    sjr: Union[float, None] = None


class SjrHit(BaseSchemas):
    sid: str
    year: int
    rank: int
    hix: int = None
    issn: Union[List[str], str, None]
    ename: str
    type: str
    fq: Union[str, None] = None
    sjr: Union[float, None] = None
    country: str = None
    region: str = None
    sjrs: Union[List[SjrRow], None] = None
    publisher: str

    @validator('fq')
    def check_fq(cls, val):
        if not val:
            return None
        if val == '-':
            return None
        return val

    @validator('sjr')
    def check_sjr(cls, val):
        if isinstance(val, float):
            return val
        if ',' in val:
            return float(val.replace(',', '.'))
        return val or None

    @validator('issn')
    def check_issn(cls, val):
        if not val.strip():
            return None
        issn_list = val.split(', ')
        data = []
        for sn in issn_list:
            if len(sn) == 8:
                data.append(sn[:4] + '-' + sn[4:])
        return data

    def load_sjrs(self) -> List[SjrRow]:
        data = []
        params = {
            "q": self.sid,
            "tip": "sid"
        }
        response = requests.get(SJR_QUERY, params=params)
        doc = Selector(response.text)
        response.close()

        sjr_list = doc.xpath('//div[@class="cell1x1 dynamiccell"][1]//tr')[1:]
        sjr = sjr_list.xpath('.//text()').get('')
        if sjr:  # 判断是否有SJR数据
            for td in sjr_list:
                year = td.xpath("./td[1]/text()").get()
                sjr = td.xpath("./td[2]/text()").get()
                row = SjrRow(year=int(year), sjr=float(sjr))
                data.append(row)
        return data
