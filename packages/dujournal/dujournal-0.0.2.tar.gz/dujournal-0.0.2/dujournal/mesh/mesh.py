# -*- coding: utf-8 -*-
# @project: dujournal
# @Author：dyz
# @date：2024/1/16 14:42
import re
from pathlib import Path

from du_aio_tools.base_spider import AioSpider
from du_aio_tools.time import timer
from parsel import Selector

from schema.mesh import MeshHit


class Mesh(AioSpider):
    def __init__(self, path: Path):
        super().__init__()
        self.url = 'https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/'
        self.text_url = 'https://www.ncbi.nlm.nih.gov/mesh/'
        self.path = path
        self.category = {
            'desc': 'desc',  # 主题词
            'supp': 'supp',  # 补充概念
            'qual': 'qual',  # 副主题词
        }

    async def download_zip(self):
        """下载 zip 数据包"""
        resp = await self.aio_get(self.url)
        doc = Selector(resp.text)
        list_xml_file = doc.xpath('//a[contains(text(),".xml")]')
        for file in list_xml_file:
            name = file.xpath('./text()').get('').strip()
            href = file.xpath('./@href').get('').strip()
            file_path = Path(self.path, name)
            # print(name, href)
            await self.aio_download(self.url + href, file_path)

    async def load_text(self, uid):
        """加载text
        https://www.ncbi.nlm.nih.gov/mesh/?term=D000001&report=Full&format=text
        """
        params = {
            'term': uid,
            'report': 'Full',
            'format': 'text',
        }
        resp = await self.aio_get(self.text_url, params=params)
        text_list = re.findall('<pre>(.*?)</pre>', resp.text, flags=re.M | re.S)
        if text_list:
            return text_list[0]
        return None

    async def parse(self, uid) -> [None, tuple]:
        """解析 text"""
        text = await self.load_text(uid)
        if text:
            tr = self.get_tr(text)
            aq = self.get_aq(text)
            return tr, aq, text
        return None

    def get_tr(self, text):
        """从下载好的网页中提取树状结构
        部分主题词后面 带一个空格加号 ' +'， 匹配主题词id时需要注意
        """
        tr_text = '    ' + text[text.find('All MeSH Categories'):]
        data_list = []
        for line in tr_text.splitlines():
            if line.strip():
                # 用每一行前面的空格数量来判断文字的位置
                index = ((len(line) - len(line.lstrip(' '))) // 4) - 1
                if index == -1:
                    break
                data_list.append((index, line.strip()))
        return data_list

    def get_aq(self, text) -> list:
        """ 获取副主题词 """
        data_list = []
        text_list = text.splitlines()
        sta = False
        for row in text_list:
            if 'Subheadings:' == row.strip():
                sta = True
                continue
            if sta:
                if not row.strip():
                    break
                name = row.strip()
                data_list.append(name)
        return data_list

    async def test(self):
        await self.download_zip()


if __name__ == '__main__':
    path = Path(__file__).parent
    mesh = Mesh(path)
    import asyncio

    # asyncio.run(mesh.test())
    asyncio.run(mesh.parse('D000001'))

