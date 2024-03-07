# -*- coding: utf-8 -*-
# @time: 2024/3/5 15:09
# @author: Dyz
# @file: esi.py
# @software: PyCharm
import re
import io
from datetime import datetime
from typing import List

import pandas as pd
from parsel import Selector
from du_aio_tools.base_spider import AioSpider

from schema.jcr import EsiHit


class EsiJour(AioSpider):
    """ESI 期刊"""

    def __init__(self):
        super().__init__()
        self.suffix = '.xlsx'
        self.url = 'https://esi.help.clarivate.com/Content/journal-list.htm'
        self.download_url = 'https://esi.help.clarivate.com/Content/'

    async def all(self):
        """获取所有年份的数据"""
        resp = await self.aio_get(self.url)
        async for row in self.parse(resp):
            yield row

    async def parse(self, resp):
        """解析数据"""
        doc = Selector(resp.text)
        href = doc.css('#mc-main-content > p:nth-child(2) > a::attr(href)').get('').strip()
        text = doc.xpath('string(//*[@id="mc-main-content"]/p[2])').get('').strip()
        data = re.findall('The current extraction date for the journal list is (.*?)\.', text, flags=re.S | re.I)
        date_obj = str(datetime.strptime(data[0], '%B %d, %Y').date())
        url = self.download_url + href
        resp = await self.aio_get(url)
        df = pd.read_excel(resp.content, keep_default_na=False)
        for row in df.to_dict('records'):
            abbr = row.get('journal title', '') or row.get('Title20', '')
            abbr2 = row.get('title29', '') or row.get('Title29', '')
            category = row.get('category name', '') or row.get('Category Name', '')
            if category:
                yield EsiHit(esi_date=date_obj, abbr=abbr, abbr2=abbr2, category=category)

    async def test(self):
        async for row in self.all():
            print(row)


if __name__ == '__main__':
    esi = EsiJour()
    import asyncio

    res = asyncio.run(esi.test())
