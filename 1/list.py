#!/usr/bin/env python3

import json
from collections import defaultdict

with open('bgg_data_clean.json') as f:
    games = json.load(f)

cols  = games['columns']
index = games['index']
data  = games['data']

for i,x in enumerate(cols):
    locals()['i_'+x] = i

class cnt:
    def __init__(self):
        self.n = 0
        self.r = [0,0]
    def __iadd__(self,g):
        self.n += 1
        self.r[0] += g[i_rating]
        self.r[1] += g[i_bayes_rating]
        return self

cnt_all = [ defaultdict(cnt), defaultdict(cnt) ]
cnt_yearly = [ [ defaultdict(cnt), defaultdict(cnt) ] for _ in range(22) ]

for g in data:
    year = g[i_year]-2000
    for x in g[i_mechanics]:
        cnt_all[0][x] += g
        cnt_yearly[year][0][x] += g
    for x in g[i_categories]:
        cnt_all[1][x] += g
        cnt_yearly[year][1][x] += g

# print('*** mechanics:')
# for x,n in sorted(mechs.items(),key=lambda x: x[1],reverse=True):
#     print(f'{n}: {x}')
#
# print('\n*** categories:')
# for x,n in sorted(cats .items(),key=lambda x: x[1],reverse=True):
#     print(f'{n}: {x}')

def dump(d):
    return [
        [ k, v.n, v.r[0]/v.n, v.r[1]/v.n ]
        for k,v in sorted(d.items(),key=lambda x: x[1].n,reverse=True) ]

with open('characteristics_frequency.json','w') as f:
    json.dump({
        'all': [ dump(d) for d in cnt_all ],
        'yearly': [ [ dump(d) for d in ds ] for ds in cnt_yearly ]
    },f,separators=(',',':'))

