# -*- coding: utf-8 -*-
# @project: dujournal
# @Author：dyz
# @date：2024/1/16 14:42
from typing import List

from Bio import Entrez

from parse_xml.parse_journal import ParseJournals


class PubMed:
    def __init__(self):
        self.db = 'nlmcatalog'

        # {"11":"NCBI", "5":"护理刊","4":"MedLine","3":"CORE","2":"PMC","1":"PubMed"}
        self.category = {
            "PUB": "ncbijournals[All Fields]",  # 所有刊检索式 11
            "NU": '("nursing"[Subheading] OR  "nursing"[All Fields] OR "nursing"[MeSH Terms]  OR "nursing"[All Fields] '
                  'OR "breast feeding"[MeSH Terms]  OR  ("breast"[All Fields] AND "feeding"[All Fields]) '
                  'OR breast feeding"[All Fields] OR Nursing[All Fields]) AND ncbijournals[All Fields]',  # 护理刊检索式
            "MD": "currentlyindexed[All]",  # MedLine刊检索式
            # "CR": "jsubsetaim[All Fields]",  # CORE刊检索式, 已经被移除
            "PA": "journalspmc[All Fields]",  # PMC刊检索式
            "PJ": "nlmcatalog pubmed[subset]",  # PubMed刊子集检索式
        }

    def all_ids(self, limit=9998) -> dict:
        """获取所有id"""
        for k, v in self.category.items():
            handle = Entrez.esearch(db=self.db, term=v, retmax=1)
            record = Entrez.read(handle)
            count = int(record['Count'])
            if count > limit:
                for i in range(0, count, limit):
                    handle = Entrez.esearch(db=self.db, term=v, retstart=i, retmax=limit)
                    record = Entrez.read(handle)
                    yield k, record['IdList']
            else:
                handle = Entrez.esearch(db=self.db, term=v, retmax=limit)
                record = Entrez.read(handle)
                yield k, record['IdList']

    def query(self, sn=None, uid=None, db=None):
        """查找PubMed 期刊
            sn 之查找 issn 相关的期刊
            uid 可以 传入 字符串/列表
        """
        db = db or self.db
        if uid:
            if isinstance(uid, list):
                count = len(uid)
            else:
                count = 10
            handle = Entrez.efetch(db=db, id=uid, retmax=count, retmode='xml')
            record = handle.read().decode('utf-8')
            pj = ParseJournals(record)
            handle.close()
            return pj.parse()
        else:
            handle = Entrez.esearch(db=db, term=f'{sn}[All Fields]', retmax=10)
            record = Entrez.read(handle)
            count = int(record['Count'])
            if count >= 1:
                handle = Entrez.efetch(db=db, id=record['IdList'], retmax=count, retmode='xml')
                record = handle.read().decode('utf-8')
                pj = ParseJournals(record)
                handle.close()
                return pj.parse()

    def day_update(self):
        """日更新"""
        # todo


if __name__ == '__main__':
    pub = PubMed()
    Entrez.email = 'xcy@xcy.club'
    Entrez.api_key = '8881d9d0222b33048a5d4a21d4b49ee56f08'
    # data = {}
    # for (k, ids) in pub.all_ids():
    #     if not data.get(k):
    #         data[k] = []
    #     data[k] += ids
    # print(len(data['PUB']))
    # print(len(set(data['PUB'])))

    res = pub.query('2277-338X')
    print(res)
