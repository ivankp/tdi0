#!/bin/bash
# https://boardgamegeek.com/wiki/page/BGG_XML_API#

mkdir -p bgg

for ((i=0; i<200000; i+=100)); do
  echo $i
  f="bgg/${i}.xml"
  if [ ! -f "$f" ]; then
    curl -L "http://www.boardgamegeek.com/xmlapi/boardgame/$(seq -s, $i $((i+99)))?stats=1" \
    | sed 's/\s\+$//;/^$/d' \
    > "$f"
  fi
done

