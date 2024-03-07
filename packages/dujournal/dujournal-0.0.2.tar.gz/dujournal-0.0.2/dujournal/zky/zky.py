# -*- coding: utf-8 -*-
# @project: dujournal
# @Author：dyz
# @date：2024/1/16 14:41
from datetime import datetime

from du_aio_tools.base_spider import AioSpider

from schema.zky import ZkyHit


def get_now_year():
    """获取当前的年份"""
    return datetime.now().year


class Zky(AioSpider):
    """
    中科院数据
    会返回三种状态
        1. null > http 200
        2. { "Message": "出现错误。" } > http 500
        3. {'Title': 'Urogynecology', 'AbbrTitle': 'UROGYNECOLOGY', 'ISSN': '2771-1897', 'Review': False, 'Year': 2023,
        'ZKY': [{'Top': False, 'Name': '医学', 'Section': 3}],
        'JCR': [{'NameCN': '妇产科学', 'Name': 'OBSTETRICS & GYNECOLOGY', 'Section': 3}], 'Indicator': None} > http 200
    """

    def __init__(self):
        super().__init__()
        self.start_year = 2005  # 中科院数据开始的年份
        self.start_v2_year = 2020  # 升级版开始的年份
        self.ZKY_QUERY = 'https://webapi.fenqubiao.com/api/journal'

    def get_params(self, abbr, year):
        params = {"abbr": abbr, "year": year}
        if not params["year"]:
            params['year'] = get_now_year()
        if params['year'] >= self.start_v2_year:
            params['version'] = 2
        return params

    def responses(self, resp, **kwargs):
        """可以再次处理相关异常"""
        if resp.status_code == 500:
            return None
        if not resp.json():
            return None
        return resp.json()

    async def query(self, abbr, year=None):
        """查询中科院数据"""
        params = self.get_params(abbr, year)
        data = await self.aio_get(self.ZKY_QUERY, params=params)
        if not data and not year:
            params['year'] -= 1
            data = await self.aio_get(self.ZKY_QUERY, params=params)
        if data:
            return ZkyHit(
                ename=data["Title"],
                abbr=data["AbbrTitle"],
                issn=data["ISSN"],
                year=data["Year"],
                zky_big=data["ZKY"],
                zky_small=data["JCR"],
                data=data
            )


if __name__ == '__main__':
    zky = Zky()
    import asyncio

    res = asyncio.run(zky.query('UROGYNECOLOGY', year=2024))
    print(res)
