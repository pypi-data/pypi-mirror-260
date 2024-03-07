# -*- coding: utf-8 -*-
# @project: dujournal
# @Author：dyz
# @date：2024/1/16 14:42
from datetime import datetime, date
from typing import List

from parsel import Selector
from du_aio_tools.base_spider import AioSpider
from tqdm import tqdm

from jcr.jcr_login import get_cookies
from schema.jcr import JcrHit


class JcrSpider(AioSpider):
    def __init__(self, user=None, pwd=None, cookies=None, headers=None):
        super().__init__(headers=headers)
        self.update_url = 'https://jcr.help.clarivate.com/Content/data-updates.htm'  # 更新公告
        self.search_url = 'https://jcr.clarivate.com/api/jcr3/bwjournal/v1/search-result'  # 检索链接
        self.user = user
        self.pwd = pwd
        if not self.headers:
            self.headers = {"Connection": "keep-alive", "Content-Type": "application/json",
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        self.cookies = cookies
        self.login_url = 'https://jcr/login'
        self.year = 0
        self.limit = 200
        self.ed_list = ["SCIE", "ESCI", "SSCI", "AHCI"]
        self.query_data = {"journalFilterParameters": {"query": "", "journals": [], "categories": [], "publishers": [],
                                                       "countryRegions": [], "citationIndexes": self.ed_list,
                                                       "jcrYear": self.get_year(), "categorySchema": "WOS",
                                                       "openAccess": "N",
                                                       "jifQuartiles": [], "jifRanges": [], "jifPercentileRanges": [],
                                                       "jciRanges": [], "oaRanges": [], "issnJ20s": []},
                           "retrievalParameters": {"start": 1, "count": self.limit, "sortBy": "jif2019",
                                                   "sortOrder": "DESC"}}

    async def login(self, reset=False, auth=None, ws=None):
        """登录 JCR"""
        cookies = await get_cookies(reset=reset, auth=auth, ws=ws)
        self.headers['Cookie'] = cookies.get("cookies")
        self.headers['x-1p-inc-sid'] = cookies.get("pid")

    def get_year(self):
        return self.year

    async def get_jcr_now_year(self) -> date:
        """获取JCR现在的最新年份"""
        resp = await self.aio_get(self.update_url)
        doc = Selector(resp.text)
        div_list = doc.css('#mc-main-content > div')
        date_list = []
        for div in div_list:
            # October 18, 2023
            text = div.xpath('./span/a/text()').get('').strip()
            date_obj = datetime.strptime(text, '%B %d, %Y').date()
            # 打印年份
            date_list.append(date_obj)
        max_date = max(date_list)
        self.year = max_date.year - 1
        self.query_data['journalFilterParameters']['jcrYear'] = self.year
        return max_date

    def responses(self, resp, **kwargs):
        """可以再次处理相关异常"""
        if self.search_url in str(resp.url):
            if resp.status_code >= 400:
                return None
            if not resp.json():
                return None
            return resp.json()
        return resp

    async def is_login(self, year=2022) -> bool:
        """测试登录是否存在
            test_year: 2022
        """
        await self.login()
        self.year = year
        self.query_data['journalFilterParameters']['jcrYear'] = year
        data = await self.aio_post(self.search_url, json=self.query_data,
                                   headers=self.headers)

        if data:
            return True
        return False

    async def all(self, year: int = None):
        """获取所有数据
        year: 这一年的数据，默认获取最新一年的数据
        """
        if year:
            self.year = year
        else:
            now_date = await self.get_jcr_now_year()
        data_list = await self.aio_post(self.search_url, json=self.query_data,
                                        headers=self.headers)
        total = data_list['totalCount']
        print("total:", total)
        for row in data_list['data']:
            yield self.parse(row)
        for start in tqdm(range(201, total + 1, self.limit)):
            json_data = self.query_data.copy()
            json_data['retrievalParameters']['start'] = start
            data_list = await self.aio_post(self.search_url, json=self.query_data,
                                            headers=self.headers, cookies=self.cookies)
            for row in data_list['data']:
                yield self.parse(row)
            # start_id += self.limit
            # if start_id > total:
            #     break

    def parse(self, data) -> JcrHit:
        """解析数据"""
        item = JcrHit(
            ename=data['journalName'],
            abbr=data['abbrJournal'],
            year=self.year,
            issn=data['issn'],
            eissn=data['eissn'],
            yx=data['jif2019'],
        )
        return self.get_ranks(data, item)

    def get_ranks(self, data, item) -> JcrHit:
        edition = []
        item.zone_rank = []
        item.fq = []
        data_list = data.get('categoryQuartiles', [])

        for row in data_list:
            category, ed = row['category'].split(' - ')
            rank = dict(year=self.year, categoryName=category, edition=ed, jifQuartile=row['quartile'],
                        jifPercentile=row['jifPercentile'], jciPercentile=row['jciPercentile'],
                        jifRank=row['jifRank'], jciRank=row['jciRank'])

            fq = dict(year=self.year, category=category, jifRank=row['jifRank'], edition=ed,
                      quartile=row['quartile'], rank=row['jifRank'], )
            item.zone_rank.append(rank)
            edition.append(ed)
            item.fq.append(fq)
        item.edition = edition
        return item

    async def test(self):
        a = 0
        # total: 21762
        async for row in self.all():
            # print(row)
            a += 1
        print(a)  # 21762


if __name__ == '__main__':
    import asyncio

    jcr = JcrSpider()
    res = asyncio.run(jcr.is_login())
