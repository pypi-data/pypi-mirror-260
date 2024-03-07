# -*- coding: utf-8 -*-
# @time: 2024/1/26 9:46
# @author: Dyz
# @file: sjr.py
# @software: PyCharm
# 检索url % issn
import re
import logging
from typing import List, Union

import httpx
import requests
import pandas as pd
from pathlib import Path
from parsel import Selector

from schema.sjr import SjrHit, SjrRow

logger = logging.getLogger('dujournal.sjr')

title_dict = {
    'Rank': 'rank',  # 排名
    'Sourceid': 'sid',  # sjr id
    'Title': 'ename',  # 刊名
    'Type': 'type',  # 类型： 期刊/?
    'Issn': 'issn',  # 期刊
    'SJR': 'sjr',  # sjr
    'SJR Best Quartile': 'fq',  # sjr fq
    'H index': 'hix',  # hix
    'Country': 'country',  # 国家
    'Region': 'region',  # 地区
    'Publisher': 'publisher',  # 出版商
}


def new_data(row):
    item = {}
    for k, v in row.items():
        if k in title_dict:
            item[title_dict[k]] = v
    return item


class Sjr:
    def __init__(self, path: Path):
        # https://www.scimagojr.com/journalrank.php?out=xls
        self.download_url = 'https://www.scimagojr.com/journalrank.php'
        self.info_url = 'https://www.scimagojr.com/journalsearch.php'
        self.path = path
        self.start_year = 1999

        self.end_year = self.max_year()

    def max_year(self) -> int:
        res = requests.get(self.download_url)
        doc = Selector(res.text)
        max_year = doc.css('#rankingcontrols > div:nth-child(5) > ul > li:nth-child(1) > a::text').get('')
        return int(max_year)

    def query(self, params):
        res = requests.get(self.info_url, params=params)
        doc = Selector(text=res.text)
        res = doc.css("div.pagination ::text").get('').strip()  # 1 - 1 of 1
        number = res.split('of ')[1]
        if number == '1':
            href = doc.css('div.search_results > a ::attr(href)').get('').strip()
            return re.findall('q=(.*?)&', href)[0]
        return False

    def info(self, sid):
        params = {"q": sid, "tip": 'sid', }
        res = requests.get(self.info_url, params=params)
        doc = Selector(res.text)
        ty = doc.xpath('//h2[text()="Publication type"]/following::p[1]/text()').get('').strip()
        issn = doc.xpath('//h2[text()="ISSN"]/following::p[1]/text()').get('').strip()
        ename = doc.xpath('//h1/text()').get('').strip()
        country = doc.xpath('//h2[text()="Country"]/following::p[1]/a/text()').get('').strip()
        hix = doc.css('p.hindexnumber::text').get('').strip()
        publisher = ''
        year = 0
        sjr_list = doc.xpath('//div[@class="cell1x1 dynamiccell"][1]//tr')[1:]
        sjr_text = sjr_list.xpath('.//text()').get('')
        data = []
        sjr = None
        if sjr_text:  # 判断是否有SJR数据
            for td in sjr_list:
                year = td.xpath("./td[1]/text()").get()
                sjr = float(td.xpath("./td[2]/text()").get())
                row = SjrRow(year=int(year), sjr=sjr)
                data.append(row)
        row = SjrHit(
            hix=int(hix),
            issn=issn,
            ename=ename,
            country=country,
            year=year,
            sjr=sjr,
            sjrs=data,
            publisher=publisher,
            sid=sid, type=ty, rank=0)
        return row

    def get_sjr(self, issn=None, eissn=None) -> Union[SjrHit, None]:
        """获取SJR数据"""
        params = {"q": issn.replace('-', '')}
        sid = self.query(params)
        if not sid and eissn:
            params = {"q": issn.replace('-', '')}
            sid = self.query(params)
        if sid:
            return self.info(sid)
        return None

    def get_year_all(self, year, file) -> Path:
        params = {"year": year, "out": "xls"}
        res = requests.get(self.download_url, params=params, stream=True)

        abs_file = Path(self.path, file)
        with open(abs_file, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
        return abs_file

    def all(self, delete=False) -> SjrHit:
        """
        :param delete: 读取之后是否删除文件，默认不删除
        :return: SjrHit
        """
        for year in range(self.start_year, self.end_year + 1):
            file = Path(f'sjr_{year}.csv')
            if not file.exists():
                file = self.get_year_all(year, file)
            df = pd.read_csv(file, sep=';', iterator=True, chunksize=50, keep_default_na=False)
            # 逐行处理数据
            for chunk in df:
                chunk_list = chunk.to_dict('records')
                for row in chunk_list:
                    data = new_data(row)
                    try:
                        yield SjrHit(**data, year=year)
                    except Exception as e:
                        logger.error(f'数据异常：{e}-{data}')
            if delete:
                file.unlink()  # 删除文件


if __name__ == '__main__':
    path = Path(__file__).parent
    sjr_obj = Sjr(path)
    print(sjr_obj.max_year())
    res = sjr_obj.get_sjr('1004-9649')
    print(res)
    print(res.load_sjrs())
    # for i in sjr_obj.all():
    #     print(i)
    #     input('aa')
