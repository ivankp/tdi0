#!/usr/bin/env python3

import re, json
from glob import glob
from lxml import etree

data  = [ ]
index = [ ]
games = {
    'columns': [
        'year',
        'age','num_players','duration',
        'mechanics','categories','families',
        'num_expansions','num_honors','num_episodes',
        'poll_age','poll_numpl',
        'num_rated','num_comments',
        'rating','bayes_rating'
    ],
    'index': index,
    'data': data
}

def try_apply(x,f,v0=None):
    try:
        return f(x)
    except:
        return v0

def get_xpath(g,p,f=lambda x: x):
    return try_apply( g.xpath(p), lambda x: f(x[0].text) )

def map_xpath(g,p,f=lambda x: x):
    return [ try_apply(x.text,f) for x in g.xpath(p) ]

def split_ints(s):
    return [ int(x) if i%2 else x for i,x in enumerate(re.split(r'(\d+)',s)) ]

def parse_suggested_playerage(x):
    n = x.get('value')
    try:
        n = int(n)
    except ValueError:
        if n == '21 and up':
            n = 21
        else:
            raise
    return [ n, int(x.get('numvotes')) ]

def parse_suggested_numplayers(x):
    n = x.get('numplayers')
    try:
        n = int(n)
    except ValueError:
        m = re.match(r'(\d+)\+$',n)
        if not (m is None):
            n = int(m.group(1))
        elif n == '+':
            return [ ]
        else:
            raise
    return [ n, [
        try_apply(x.xpath(f'result[@value="{v}"]'),
            lambda x: int(x[0].get('numvotes'))
        ) for v in ['Best','Recommended','Not Recommended']
    ] ]

for fname in sorted(glob('bgg/*.xml'),key=split_ints):
    print(fname)
    for g in etree.parse(fname).xpath('/boardgames/boardgame'):
        x = g.get('objectid')
        if x is None: continue

        index.append(int(x))
        stat = g.xpath('statistics/ratings')[0]
        data.append([
            get_xpath(g,'yearpublished',int),
            get_xpath(g,'age',float),
            [ get_xpath(g,'minplayers',int),
              get_xpath(g,'maxplayers',int) ],
            [ get_xpath(g,'playingtime',float),
              get_xpath(g,'minplaytime',float),
              get_xpath(g,'maxplaytime',float) ],
            map_xpath(g,'boardgamemechanic'),
            map_xpath(g,'boardgamecategory'),
            map_xpath(g,'boardgamefamily'),
            len(g.xpath('boardgameexpansion')),
            len(g.xpath('boardgamehonor')),
            len(g.xpath('boardgamepodcastepisode')),
            [ parse_suggested_playerage(x) for x in
                g.xpath('poll[@name="suggested_playerage"]/results/result') ],
            [ parse_suggested_numplayers(x) for x in
                g.xpath('poll[@name="suggested_numplayers"]/results') ],
            get_xpath(stat,'usersrated',int),
            get_xpath(stat,'numcomments',int),
            get_xpath(stat,'average',float),
            get_xpath(stat,'bayesaverage',float)
        ])

print(f'num games: {len(data)}')

with open('bgg_data.json','w') as f:
    json.dump(games,f,separators=(',',':'))

