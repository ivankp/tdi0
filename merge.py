#!/usr/bin/env python3

from lxml import etree
import re, json

games = [
    ['id','year',
     'minplayers','maxplayers',
     'playingtime','minplaytime','maxplaytime',
     'age',
     'mechanics','categories','families','expansions',
     'poll_age','poll_numpl'
    ]
]

def try_convert(x,f,x0=None):
    try:
        return f(x)
    except:
        return x0

for fi in range(1,9000):
    g = etree.parse(f'bgg/{fi}.xml')
    g = g.xpath('/boardgames/boardgame')[0]
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

    games.append(game)

# for g in games:
#     print(g)

with open('bgg_data.json','w') as f:
    json.dump(games,f,separators=(',',':'))
