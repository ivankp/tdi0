#!/usr/bin/env python3
import sys, json, requests
from pytrends.request import TrendReq

tr = TrendReq(hl='en-US',tz=240)
# ac = tr.suggestions(keyword='The Quest for El Dorado')
ac = tr.suggestions(keyword='Dominion')
print(ac)
mid = ac[0]['mid']
print(mid)
mid = requests.utils.quote(mid)
print(mid)

tr.build_payload(kw_list=[mid])
print(tr.interest_over_time())


