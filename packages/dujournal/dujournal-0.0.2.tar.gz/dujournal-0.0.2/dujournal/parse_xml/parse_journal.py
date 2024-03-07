# -*- coding: utf-8 -*-
# @time: 2024/3/4 11:03
# @author: Dyz
# @file: parse_journal.py
# @software: PyCharm
from datetime import date
from typing import List

from parsel import Selector
from schema.jouornal import JournalHit, RelJournal

JOURNAL_INDEX = ["MEDLINE", "PubMed", "PMC"]


def parse_date(doc):
    if doc:
        year = int(doc.xpath('./Year/text()').get())
        month = int(doc.xpath('./Month/text()').get())
        day = int(doc.xpath('./Day/text()').get())
        if year:
            return date(year=year, month=month, day=day)
    return None


class ParseJournal:
    def __init__(self, xml: str = None, doc=None):
        if xml:
            doc = Selector(xml, type='xml')
            self.doc = doc.xpath('/NLMCatalogRecordSet/NLMCatalogRecord')
        else:
            self.doc = doc
        self.data = JournalHit(id=self.doc.xpath('./NlmUniqueID/text()').get())

    def parse_date(self):
        """解析时间相关数据"""
        self.data.date_created = parse_date(self.doc.xpath('./DateCreated'))
        self.data.date_revised = parse_date(self.doc.xpath('./DateRevised'))
        self.data.date_authorized = parse_date(self.doc.xpath('./DateAuthorized'))
        self.data.date_completed = parse_date(self.doc.xpath('./DateCompleted'))
        self.data.date_revised_major = parse_date(self.doc.xpath('./DateRevisedMajor'))

    def parse_publication(self):
        """出版物类型"""
        _data = []
        pt_list = self.doc.xpath('./PublicationTypeList')
        for row in pt_list:
            text = row.xpath('./text()').get('').strip()
            if text:
                _data.append(text)
        self.data.publication_type = _data

    def parse_publication_info(self):
        """出版信息"""
        _data = []
        p_info_doc = self.doc.xpath('./PublicationInfo')
        self.data.country = p_info_doc.xpath('./Country/text()').get('').strip() or None
        self.data.place_code = p_info_doc.xpath('./PlaceCode/text()').get('').strip() or None
        self.data.publication_first_year = p_info_doc.xpath('./PublicationFirstYear/text()').get('').strip() or None
        self.data.publication_end_year = p_info_doc.xpath('./PublicationEndYear/text()').get('').strip() or None
        self.data.frequency = p_info_doc.xpath('./Frequency/text()').get('').strip() or None

    def parse_index(self):
        """解析索引"""
        _data = []
        index_list = self.doc.xpath('./IndexingSourceList/IndexingSource')
        for row in index_list:
            text = row.xpath('./IndexingSourceName/text()').get('').strip()
            if text in JOURNAL_INDEX:
                if text == 'MEDLINE':
                    status = row.xpath('./IndexingSourceName/@IndexingStatus').get('').strip()
                    if status == 'Currently-indexed':
                        _data.append(text)
                else:
                    _data.append(text)
        self.data.index_list = _data

    def mash(self):
        """解析期刊中的主题词"""
        mesh_list = []
        mesh_doc = self.doc.xpath('./MeshHeadingList/MeshHeading')
        for row in mesh_doc:
            desc = row.xpath('./DescriptorName/text()').get('').strip()
            q = row.xpath('./QualifierName/text()').get('').strip()
            if q:
                desc += f'/{q}'
            mesh_list.append(desc)
        self.data.mesh = mesh_list

    def parse_language(self):
        """解析语言"""
        _data = []
        note_list = self.doc.xpath('./Language')
        for row in note_list:
            lang_type = row.xpath('./@LangType').get('')
            if lang_type == 'Primary':
                text = row.xpath('./text()').get('').strip()
                if text:
                    _data.append(text)
        self.data.language = _data

    def parse_title(self):
        """解析标题相关"""
        _data = []
        self.data.title = self.doc.xpath('./TitleMain/Title/text()').get('').strip()
        self.data.title_alternate = self.doc.xpath('./TitleAlternate/Title/text()').get('').strip()
        self.data.title_alternate = self.doc.xpath('./TitleAlternate/Title/text()').get('').strip()
        self.data.abbr = self.doc.xpath('./MedlineTA/text()').get('').strip()

    def parse_note(self):
        """解析 Note"""
        _data = []
        note_list = self.doc.xpath('./GeneralNote')
        for row in note_list:
            text = row.xpath('./text()').get('').strip()
            if text:
                _data.append(text)
        self.data.note = _data

    def parse_link(self):
        _data = []
        link_list = self.doc.xpath('./ELocationList/ELocation')
        for row in link_list:
            text = row.xpath('./ELocationID/text()').get('').strip()
            if text:
                _data.append(text)
        self.data.elink = _data

    def parse_issn(self):
        issn_list = self.doc.xpath('./ISSN')
        for row in issn_list:
            text = row.xpath('./text()').get('').strip()
            issn_type = row.xpath('./@IssnType').get('').strip()
            if issn_type == 'Print':
                self.data.issn = text
            elif issn_type == 'Electronic':
                self.data.issn = text
        self.data.lissn = self.doc.xpath('./ISSNLinking/text()').get('').strip()

    def parse_r_jour(self):
        """解析相关期刊"""
        _data_list = []
        rj_list = self.doc.xpath('./TitleRelated')
        for row in rj_list:
            ty = row.xpath('./@TitleType').get('').strip() or None
            ti = row.xpath('./Title/text()').get('').strip() or None
            id_ = row.xpath('./RecordID/text()').get('').strip() or None
            issn = row.xpath('./ISSN/text()').get('').strip() or None
            _data_list.append(RelJournal(title=ti, id=id_, issn=issn, type=ty))
        self.data.title_related = _data_list

    def parse(self) -> JournalHit:
        self.parse_date()
        self.parse_publication()
        self.parse_publication_info()
        self.parse_index()
        self.mash()
        self.parse_language()
        self.parse_title()
        self.parse_note()
        self.parse_link()
        self.parse_issn()
        self.parse_r_jour()
        return self.data


class ParseJournals:
    def __init__(self, xml: str):
        self.doc = Selector(xml, type='xml')
        self.list = self.doc.xpath('/NLMCatalogRecordSet/NLMCatalogRecord')

    def parse(self) -> List[JournalHit]:
        data_list = []
        for doc in self.list:
            parse = ParseJournal(doc=doc)
            data_list.append(parse.parse())
        return data_list
