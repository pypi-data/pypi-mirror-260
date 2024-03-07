# -*- coding: utf-8 -*-
# @project: dujournal
# @Author：dyz
# @date：2024/1/16 14:44
from typing import Union

from crossref.restful import Journals
from du_aio_tools.rsa import make_md5

from schema.jouornal import JournalDoiHit


def parse(data: dict) -> Union[None, JournalDoiHit]:
    if data.get('issn-type'):
        item = JournalDoiHit()
        # issn
        for sn in data['issn-type']:
            if sn.get('type') == 'print':
                item.issn = sn['value']
            elif sn.get('type') == 'electronic':
                item.eissn = sn['value']
        item.id = make_md5(item.issn or item.eissn)

        # 发表卷期的年份
        if data.get('breakdowns', {}).get('dois-by-issued-year'):
            year_list = [_[0] for _ in data['breakdowns']['dois-by-issued-year']]
            item.publication_first_year = min(year_list)
            item.publication_end_year = max(year_list)

        item.title = data['title']

        # 主题词
        if data.get('subjects'):
            mesh, tn = [], []
            for ms in data['subjects']:
                mesh.append(ms['name'])
                tn.append(str(ms['ASJC']))
            item.mesh = ';'.join(mesh)
            item.tn = ';'.join(tn)

        return item
    return None


class DoiJournal(Journals):
    CURSOR_AS_ITER_METHOD = True

    def all_jour(self):
        for row in self.all(None):
            yield parse(row)


if __name__ == '__main__':
    jour = DoiJournal()
    res = jour.journal(issn='2277-338X')
    print(parse(res))
    # for i in jour.all_jour():
    #     print(i)
