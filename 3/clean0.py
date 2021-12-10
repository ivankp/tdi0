#!/usr/bin/env python3

import json, re

print('reading')
with open('bgg_data.json') as f:
    games = json.load(f)

cols  = games['columns']
index = games['index']
data  = games['data']

for i,x in enumerate(cols):
    locals()['i_'+x] = i

def select(g):
    year = g[i_year]
    if (year is None or year<2000 or year>2021): return False
    r = g[i_bayes_rating]
    if r is None or r<=0: return False
    return True

print('selecting')
ii = [ i for i,g in enumerate(data) if select(g) ]
print('games:',len(ii))

def fix(g):
    g[i_mechanics] = sorted(set(
        'Auction' if x.startswith('Auction') else
        'Worker Placement' if x.startswith('Worker Placement') else
        x for x in g[i_mechanics] ))
    return g

print('writing')
with open('bgg_data_clean.json','w') as f:
    json.dump({
        'columns': cols,
        'index': [ index[i] for i in ii ],
        'data': [ fix(data[i]) for i in ii ]
    },f,separators=(',',':'))

