# -*- coding: utf-8 -*-
# @project: dujournal
# @Author：dyz
# @date：2024/1/16 14:41
# 预警期刊
import re
from typing import Union, List

import requests
from parsel import Selector
from schema.zky import ZkyWarnHit


class ZkyWarn:
    def __init__(self):
        self.start_year = 2019  # 预警期刊开始年份
        self.zky_warn_url = 'https://earlywarning.fenqubiao.com/_sidebar.md'
        self.max_url = None

    def get_new_year(self, year: int = None, all_year=False) -> Union[str, List]:
        """取预警期刊的最新年份"""
        year = int(year) if year else None
        resp = requests.get(self.zky_warn_url)
        resp.encoding = resp.apparent_encoding
        html = resp.text
        max_year = 0
        data_list = []
        for i in html.split('\n'):
            i = i.strip('').lstrip('* ').strip()
            if '年预警名单]' in i:
                _year = int(re.findall('\[(\\d{4})年预警名单]', i)[0])
                url = re.findall('年预警名单]\((/zh-cn/early-warning-journal-list-\d{4}.md)', i)[0]
                href = f'https://earlywarning.fenqubiao.com{url}'
                data_list.append(href)
                if year and _year == year:
                    return href
                if _year > max_year:
                    max_year = _year
                    self.max_url = href
        if all_year:
            return data_list
        return self.max_url

    def all(self):
        """所有年份数据"""
        href_list = self.get_new_year(all_year=True)
        for href in href_list:
            resp = requests.get(href)
            resp.encoding = resp.apparent_encoding
            yield self.parse(resp.text)

    @staticmethod
    def parse(resp) -> List[ZkyWarnHit]:
        doc = Selector(resp)
        year = int(re.findall('(\\d{4})年《国际期刊预警名单', resp)[0])
        tr_list = doc.css('tbody > tr')
        data_list = []
        if year < 2024:
            for tr in tr_list:
                td_list = tr.xpath('./td')
                name = td_list[-2].xpath('./text()').get('').strip()
                level = td_list[-1].xpath('./text()').get('').strip()
                item = ZkyWarnHit(ename=name, level=level, year=year)
                data_list.append(item)
        else:
            for tr in tr_list:
                td_list = tr.xpath('./td')
                name = td_list[-3].xpath('./text()').get('').strip()
                issn = td_list[-2].xpath('./text()').get('').strip()
                level = td_list[-1].xpath('./text()').get('').strip()
                item = ZkyWarnHit(ename=name, issn=issn, level=level, year=year)
                data_list.append(item)
        return data_list

    def get_zky_warn_list(self, year=None):
        """
        获取预警名单
        year: 预警年份
        :return: List[ZkyWarnHit]
        """
        if year:
            href = self.get_new_year(year)
        else:
            href = self.get_new_year()
        resp = requests.get(href)
        resp.encoding = resp.apparent_encoding
        return self.parse(resp.text)

    def run(self):
        for data in self.all():
            print(data)


if __name__ == '__main__':
    zw = ZkyWarn()
    res = zw.run()  # year=2023
    print(res)  # > [ZkyWarnHit(year=2023, ename='TEXTILE RESEARCH JOURNAL', issn=None, level='中')
