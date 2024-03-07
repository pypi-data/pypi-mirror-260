# -*- coding: utf-8 -*-
# @project: dujournal
# @Author：dyz
# @date：2024/1/17 17:21
from datetime import date
from typing import List, Optional, Union

from du_aio_tools.schemas import BaseSchemas


class RelJournal(BaseSchemas):
    """相关期刊"""
    id: str = None
    title: str
    issn: str = None
    type: str


class LetPubHit(BaseSchemas):
    title: Union[None, str] = None
    issn: Union[None, str] = None
    hit: Union[None, str] = None  # 命中率
    introduction: Union[None, str] = None  # 审稿周期
    cycle: Union[None, str] = None  # 审稿周期
    delivery_link: Union[None, str] = None  # 投稿链接
    website_link: Union[None, str] = None  # 官网链接
    author_notice: Union[None, str] = None  # 作者须知
    p_number: Union[None, str] = None  # 出版量
    self_quote: Union[None, str] = None  # 自引率
    url: Union[None, str] = None  # 网址


class JournalDoiHit(BaseSchemas):
    id: str = ''
    title: str = ''
    # 开始出版年
    publication_first_year: Union[None, str] = None
    # 最后出版年
    publication_end_year: Union[None, str] = None
    mesh: Union[None, str] = None
    tn: Union[None, str] = None
    issn: Union[None, str] = None
    eissn: Union[None, str] = None


class JournalHit(BaseSchemas):
    id: str = ''
    title: Union[None, str] = None
    date_created: Union[None, date] = None
    date_revised: Union[None, date] = None
    date_authorized: Union[None, date] = None
    date_completed: Union[None, date] = None
    date_revised_major: Union[None, date] = None

    title_alternate: Union[None, str] = None
    title_related: List[RelJournal] = None
    abbr: Union[None, str] = None

    note: List[str] = None
    language: List[str] = None
    frequency: str = None

    # 出版类型
    publication_type: List[str] = None
    # 出版信息
    country: Union[None, str] = None
    place_code: Union[None, str] = None
    # 开始出版年
    publication_first_year: Union[None, str] = None
    # 最后出版年
    publication_end_year: Union[None, str] = None

    index_list: Union[List[str], None] = None

    elink: Union[List[str], None] = None
    issn: Union[None, str] = None
    eissn: Union[None, str] = None
    lissn: Union[None, str] = None

    mesh: Union[None, List] = None
