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
    if (r is None or r<=0): return False
    return True

print('selecting')
ii = [ i for i,g in enumerate(data) if select(g) ]
print('games:',len(ii))

fix_attrs_dict = {
    'Action / Dexterity': 'Dexterity',
    'Bluffing – Dice Cup': 'Bluffing',
    'Book': 'Books',
    'Card Games': 'Card Game',
    'Comic Book / Strip': 'Comics',
    'Connection': 'Connections',
    'Construction Toys': 'Construction',
    'Crayon Rail System': 'Crayons',
    'DVDs': 'Compact Discs (CDs)',
    'Deck Construction': 'Deck Building',
    'Deck, Bag, and Pool Building': 'Deck Building',
    'Deduction – Blind Man\'s Bluff': 'Deduction',
    'Finger Flicking Games': 'Flicking',
    'Grids': 'Grid',
    'Movies / TV / Radio theme': 'TV, Shows, Movies',
    'Real-time': 'Real-Time',
    'dice': 'Dice',
}
def fix_attrs(attrs):
    for k in list(attrs):
        v = fix_attrs_dict.get(k,None)
        if not (v is None):
            attrs.discard(k)
            attrs.add(v)
        for x in [
            'Drafting','Dice','Expansion','Flicking','Clue','Grid','Auction',
            'Asymmetric'
        ]:
            if x in k:
                attrs.add(x)
        for x in [
            'Dice Rolling'
        ]:
            if x in attrs:
                attrs.discard(x)

def collect_attrs(g):
    attrs = set()
    attrs.update(g[i_mechanics])
    attrs.update(g[i_categories])
    for x in g[i_families]:
        m = re.match(r'([^:]+):\s*(.*)',x)
        if m:
            if 'Traditional' in x:
                attrs.add('Traditional')
            if m[1] in {'Series','Creatures','Animals','Occupation','History',
                'Food & Drink', 'Rivers', 'Sports Teams', 'Sports', 'Setting',
                'Traditional Card Games', 'Ancient', 'Traditional Games',
                'Books', 'Islands', 'Video Game Theme', 'Space', 'Brands',
                'Holidays', 'Religious', 'Characters', 'Toys', 'Medical',
                'Fictional Events', 'Music', 'Historical Figures',
                'Celebrities', 'Trivia', 'Decades', 'Political', 'Contests',
                'Traditional Dice Games'
            }:
                attrs.add(m[1])
            elif m[1] in {'Mechanism','Players','Component','Misc','Category',
                'Containers'
            }:
                attrs.add(m[2])
            elif m[1] in {'Mythology','Card Games'}:
                attrs.add(m[1])
                attrs.add(f'{m[1]}: {m[2]}')
            elif m[1] in {'TV Shows', 'Movies'}:
                attrs.add('TV, Shows, Movies')
            elif m[1] in {'Comic Books', 'Webcomics', 'Comic Strips'}:
                attrs.add('Comics')
            elif m[1] in {'Region','States','Mountain','Mountains','Cities',
                'Country','Continents'
            }:
                attrs.add('Region')
            elif m[1] in {'Constructions','Construction'}:
                attrs.add('Construction')
            elif m[1] == 'Folk Tales & Fairy Tales':
                attrs.add('Folk Tales')
            elif m[1] == 'Theme':
                attrs.add('Theme')
                if m[2] in {'Mushrooms','Rivers','Vikings','Nature','Fashion',
                    'City','Art','Love / Romance'
                }:
                    attrs.add(m[2])
                elif m[2] in {'Television (TV) Industry','TV Detectives'}:
                    attrs.add('TV, Shows, Movies')
            elif m[1] == 'Components':
                for x in ['Meeples','Grids','Map','Dice','dice']:
                    if x in m[2]:
                        attrs.add(x)
                        break
                else:
                    attrs.add(m[2])
    fix_attrs(attrs)
    return attrs

def fix(g):
    g[i_mechanics] = sorted(set(
        'Auction' if x.startswith('Auction') else
        'Worker Placement' if x.startswith('Worker Placement') else
        x for x in g[i_mechanics] ))
    g2 = g.copy()
    del g2[i_mechanics:i_families+1]
    g2.append( list(collect_attrs(g)) )
    return g2

print('writing')
with open('bgg_data_clean.json','w') as f:
    cols2 = cols.copy()
    del cols2[i_mechanics:i_families+1]
    cols2.append('attrs')
    json.dump({
        'columns': cols2,
        'index': [ index[i] for i in ii ],
        'data': [ fix(data[i]) for i in ii ]
    },f,separators=(',',':'))

