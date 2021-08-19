#!/usr/bin/env python3

import json

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
    br = g[i_bayes_rating]
    if (br is None or br<=0): return False
    # if len(g[i_mechanics]) == 0: return False
    return True

print('selecting')
ii = [ i for i,g in enumerate(data) if select(g) ]

def fix(g):
    mech = g[i_mechanics]
    g[i_mechanics] = sorted(set(
        'Auction' if x.startswith('Auction') else
        'Worker Placement' if x.startswith('Worker Placement') else
        x for x in mech ))
    return g

print('games:',len(ii))

print('writing')
with open('bgg_data_clean.json','w') as f:
    json.dump({
        'columns': cols,
        'index': [ index[i] for i in ii ],
        'data': [ fix(data[i]) for i in ii ]
    },f,separators=(',',':'))

