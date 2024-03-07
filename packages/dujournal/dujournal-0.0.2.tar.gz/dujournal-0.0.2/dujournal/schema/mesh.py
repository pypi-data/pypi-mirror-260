# -*- coding: utf-8 -*-
# @project: dujournal
# @Author：dyz
# @date：2024/1/19 10:31
from datetime import date
from typing import List, Optional, Union

from du_aio_tools.schemas import BaseSchemas


class MeshHit(BaseSchemas):
    uid: str  # 主题词ID
    name: str
    note: str  # 英文解释
    tn: List[str] = None  # 树状号 Tree number
    hm: List[str] = None  # 树状号 Tree number
    # ph: str = None # ?
    ey: List[str] = None  # 入口词
    tp: str
    tr: str = None  # MeSH Categories
    aq: str = None  # 副主题词
    abbr: str = ''
