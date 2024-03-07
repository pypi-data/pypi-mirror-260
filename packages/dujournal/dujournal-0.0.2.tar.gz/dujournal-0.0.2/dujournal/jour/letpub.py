# -*- coding: utf-8 -*-
# @time: 2023/3/7 10:26
# @author: Dyz
# @file: letpub.py
# @software: PyCharm
# 投稿相关数据经过对比，梅斯数据效果不如 letpub
# 该网站数据收录只有SCI期刊数据
import re
import time

import httpx
from du_aio_tools.base_spider import AioSpider
from parsel import Selector

from schema.jouornal import LetPubHit


class Spider(AioSpider):
    def __init__(self, wait_fixed=5000):
        super().__init__()
        self.url = 'https://www.letpub.com.cn/index.php'
        self.info_url = 'http://www.letpub.com.cn/index.php?journalid={}&page=journalapp&view=detail'
        self.wait_html = ['您刷新页面的速度过快', '请求期刊页面数据过于频繁', '温馨提示：您使用的IP地址']
        self.wait_fixed = wait_fixed
        # self.headers = {
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        #     'Cache-Control': 'max-age=0',
        #     'DNT': '1',
        #     'Origin': 'http://www.letpub.com.cn',
        #     'Referer': 'http://www.letpub.com.cn/index.php?page=journalapp&view=search',
        #     'Upgrade-Insecure-Requests': '1',
        #     'User-Agent': self.get_ua()}
        # self.client = httpx.AsyncClient(limits=self.limits, verify=False)  # 异步

    def responses(self, resp, **kwargs):
        """letpub 有ip访问速度的限制"""
        html = resp.text
        for text in self.wait_html:
            if text in html:
                time.sleep(self.wait_fixed)
                raise
        return resp

    def get_params(self, sn, abbr):
        params = {
            'page': 'journalapp',
            'view': 'search',
        }

        data = {
            'searchname': abbr or '',
            'searchissn': sn or '',
            'searchfield': '',
            'searchimpactlow': '',
            'searchimpacthigh': '',
            'searchscitype': '',
            'view': 'search',
            'searchcategory1': '',
            'searchcategory2': '',
            'searchjcrkind': '',
            'searchopenaccess': '',
            'searchsort': 'relevance',
        }
        return params, data

    async def query(self, sn=None, abbr=None):
        """查找数据 """
        if not sn and not abbr:
            raise
        params, data = self.get_params(sn, abbr)
        res = await self.aio_post(self.url, params=params, json=data)
        html = res.text
        jid = re.findall('journalid=(\d+)&page=journalapp', html)
        if not jid:
            jid = re.findall('journalid=(\d+)&page=journalapp', html)
        if jid:
            url = self.info_url.format(jid[0])
            resp = await self.aio_get(url, headers=self.headers)
            item = LetPubHit(url=url, issn=sn, title=abbr)
            return self.parse(resp.text, item)

    def parse(self, html, item) -> LetPubHit:
        doc = Selector(html)
        item.introduction = doc.xpath("string(//td[contains(text(),'期刊简介')]/following-sibling::td)").get(
            '').strip()

        item.website_link = doc.xpath("string(//td[contains(text(),'期刊官方网站')]/following-sibling::td)").get(
            '').strip()

        item.delivery_link = doc.xpath(
            "string(//td[contains(text(),'期刊投稿网址')]/following-sibling::td)").get('').strip()

        item.author_notice = doc.xpath(
            "string(//td[contains(text(),'作者指南网址')]/following-sibling::td)").get('').strip()

        self_quote = doc.xpath("string(//td[contains(text(),'自引率')]/following-sibling::td)").get('').strip()
        if '%' in self_quote:
            self_quote = self_quote.split('%', 1)[0]
            if self_quote.strip():
                item.self_quote = self_quote + '%'  # 自引率

        item.hit = doc.xpath("string(//td[contains(text(),'平均录用比例')]/following-sibling::td)").get(
            '').strip().split('：')[-1]

        item.cycle = doc.xpath("string(//td[contains(text(),'平均审稿速度')]/following-sibling::td)").get(
            '').strip().split('：')[-1]
        item.p_number = doc.xpath("string(//td[contains(text(),'年文章数')]/following-sibling::td)").get(
            '').strip().split('注册')[0].split('点击查看')[0].strip()
        return item

    async def test(self, issn='0393-974X'):
        data = await self.query(issn)
        print(data)


if __name__ == '__main__':
    import asyncio

    let_pub_obj = Spider()

    asyncio.run(let_pub_obj.test(issn='0066-4154'))
