#!/usr/bin/env python3

import re, json
from glob import glob
from lxml import etree

games = [
    ['id','year',
     'minplayers','maxplayers',
     'playingtime','minplaytime','maxplaytime',
     'age',
     'mechanics','categories','families','expansions',
     'poll_age','poll_numpl',
     'numrated','numcomments','bayesaverage','average'
    ]
]

def try_convert(x,f,x0=None):
    try:
        return f(x)
    except:
        return x0

def split_ints(s):
    return [ int(x) if i%2 else x for i,x in enumerate(re.split(r'(\d+)',s)) ]

for fname in sorted(glob('bgg/*.xml'),key=split_ints):
    print(fname)
    for g in etree.parse(fname).xpath('/boardgames/boardgame'):
        x = g.get('objectid')
        if x is None:
            continue
        game = [ int(x) ]

        game.append( try_convert(g.xpath('yearpublished')[0].text,int) )
        game.append( try_convert(g.xpath('minplayers')[0].text,int) )
        game.append( try_convert(g.xpath('maxplayers')[0].text,int) )
        game.append( try_convert(g.xpath('playingtime')[0].text,float) )
        game.append( try_convert(g.xpath('minplaytime')[0].text,float) )
        game.append( try_convert(g.xpath('maxplaytime')[0].text,float) )
        game.append( try_convert(g.xpath('age')[0].text,float) )

        game.append( [ x.text for x in g.xpath('boardgamemechanic') ] )
        game.append( [ x.text for x in g.xpath('boardgamecategory') ] )
        game.append( [ x.text for x in g.xpath('boardgamefamily') ] )
        game.append( len(g.xpath('boardgameexpansion')) )

        game.append( [ [
            int(re.search(r'\d+',x.get('value')).group()),
            int(x.get('numvotes'))
        ] for x in g.xpath(
            'poll[@name="suggested_playerage"]/results/result'
        ) ] )

        game.append( [ [
            int(x.xpath(f'result[@value="{v}"]')[0].get('numvotes'))
            for v in ['Best','Recommended','Not Recommended']
        ] for x in g.xpath(
            'poll[@name="suggested_numplayers"]/results'
        ) ] )

        rt = g.xpath('statistics/ratings')[0]
        for v in ['usersrated','numcomments']:
            game.append( try_convert(rt.xpath(v)[0].text,int) )
        for v in ['bayesaverage','average']:
            game.append( try_convert(rt.xpath(v)[0].text,float) )

        games.append(game)

print(f'num games: {len(games)-1}')

with open('bgg_data.json','w') as f:
    json.dump(games,f,separators=(',',':'))
