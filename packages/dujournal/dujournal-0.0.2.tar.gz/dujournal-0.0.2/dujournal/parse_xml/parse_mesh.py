# -*- coding: utf-8 -*-
# @time: 2024/3/5 14:28
# @author: Dyz
# @file: parse_mesh.py
# @software: PyCharm
from pathlib import Path
from typing import List

from parsel import Selector

from schema.mesh import MeshHit


def row_supp(xml) -> MeshHit:
    """解析补充概念"""
    doc = Selector(xml, type='xml')
    uid = doc.xpath('.//SupplementalRecordUI/text()').get('').strip()
    name = doc.xpath('.//SupplementalRecordName/String/text()').get('').strip()
    note = doc.xpath('.//Note/text()').get('').strip()
    ey = doc.xpath('.//TermList//String/text()').getall()
    hm_list = doc.xpath('.//HeadingMappedToList//DescriptorReferredTo')
    hm = []
    for h_ in hm_list:
        hm_name = h_.xpath('.//DescriptorName/String/text()').get('').strip()
        hm_uid = h_.xpath('.//DescriptorUI/text()').get('').strip()
        if hm_name:
            hm.append(f'{hm_uid}@@{hm_name}')

    if ey and ey[0] == name:
        ey.pop(0)
    return MeshHit(
        uid=uid,
        name=name,
        note=note,
        hm=hm,
        ey=ey,
        tp='SC'
    )


def row_qual(xml) -> MeshHit:
    """解析副主题词"""
    doc = Selector(xml, type='xml')
    uid = doc.xpath('.//QualifierUI/text()').get('').strip()
    name = doc.xpath('.//QualifierName/String/text()').get('').strip()
    note = doc.xpath('.//ConceptList/Concept/ScopeNote/text()').get('').strip()
    tn = doc.xpath('.//TreeNumberList/TreeNumber/text()').getall()
    abbr = doc.xpath('.//Abbreviation/text()').get('').strip()
    return MeshHit(
        uid=uid,
        name=name,
        note=note,
        tn=tn,
        abbr=abbr,
        tp='QU',
    )


def row_desc(xml) -> MeshHit:
    """解析主题词"""
    doc = Selector(xml, type='xml')
    uid = doc.xpath('.//DescriptorUI/text()').get('').strip()
    name = doc.xpath('.//DescriptorName/String/text()').get('').strip()
    note = doc.xpath('.//ConceptList/Concept/ScopeNote/text()').get('').strip()
    tn = doc.xpath('.//TreeNumberList/TreeNumber/text()').getall()
    ey = doc.xpath('.//TermList//String/text()').getall()
    if ey and ey[0] == name:
        ey.pop(0)

    return MeshHit(
        uid=uid,
        name=name,
        note=note,
        tn=tn,
        tp='D',
        ey=ey
    )


class ParseMeshList:
    def __init__(self, file: Path = None, text: str = None):
        """
        :param file: 解析xml文件
        :param text: 解析text文本网页源码
        """
        self.file = file
        self.text = text

    def tp(self) -> str:
        """判断数类型"""
        import itertools
        text = ''
        with open(self.file, encoding='utf-8') as f:
            for line in itertools.islice(f, 4):
                if line:
                    text = line
        return text

    def parse(self):
        text = self.tp()
        if text.startswith('<Desc'):
            for row in self.parse_desc():
                yield row
        elif text.startswith('<Supp'):
            for row in self.parse_supp():
                yield row
        elif text.startswith('<Qual'):
            for row in self.parse_qual():
                yield row

    def read_line(self, text) -> str:
        """数据按行读取"""
        xml = ''
        with open(self.file, 'r', encoding='utf-8') as f:
            for line in f:
                # 每条数据的开头
                if line.startswith(text):
                    if xml:  # 如果有上一条就返回后赋予新的
                        yield xml
                        xml = line
                        continue
                    else:  # 没有上一条就直接加在一起
                        xml += line
                        continue
                if xml:
                    xml += line
            if xml:
                yield xml

    def parse_desc(self) -> List[MeshHit]:
        """解析主题词"""
        for xml in self.read_line(text='<DescriptorRecord DescriptorClass'):
            yield row_desc(xml)

    def parse_supp(self):
        """解析补充概念"""
        for xml in self.read_line(text='<SupplementalRecord SCRClass'):
            yield row_supp(xml)

    def parse_qual(self):
        """解析补充概念"""
        for xml in self.read_line(text='<QualifierRecord>'):
            yield row_qual(xml)

    def test(self):
        for row in self.parse():
            print(row)


if __name__ == '__main__':
    file = Path(r'D:\work\pypi_hub\dujournal\mesh\qual2024.xml')
    mesh = ParseMeshList(file)
    print(mesh.test())
