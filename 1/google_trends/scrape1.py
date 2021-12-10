#!/usr/bin/env python3
import sys, requests, json

s = requests.Session()

ac = s.get(
    'https://trends.google.com/trends/api/autocomplete/' +
    requests.utils.quote('The Quest for El Dorado') +
    '?hl=en-US&tz=240').text

ac = json.loads(ac[ac.find('{'):])
topics = ac['default']['topics']
topics = [ x for x in topics if x['type']=='Tabletop game' ]
if len(topics)!=1:
    print(topics)
    sys.exit(1)
mid = topics[0]['mid']
print(mid)

# page = s.get(
#     'https://trends.google.com/trends/explore?q=' +
#     requests.utils.quote(mid) +
#     '&geo=US').text
# print(page)
'https://trends.google.com/trends/api/widgetdata/multiline/csv?req={"time":"2016-08-29 2021-08-29","resolution":"WEEK","locale":"en-US","comparisonItem":[{"geo":{"country":"US"},"complexKeywordsRestriction":{"keyword":[{"type":"ENTITY","value":"/g/11fx8vn85r"}]}}],"requestOptions":{"property":"","backend":"IZG","category":0}}&token=APP6_UEAAAAAYS0qFq1wWPV0vyOOS27ROpayPoTeejTY&tz=240'
