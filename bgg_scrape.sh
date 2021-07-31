#!/bin/bash
# https://boardgamegeek.com/wiki/page/BGG_XML_API#

mkdir -p bgg

for i in {1..10000}; do
  echo $i
  f="bgg/${i}.xml"
  if [ ! -f "$f" ]; then
    curl -L "http://www.boardgamegeek.com/xmlapi/boardgame/${i}" \
    | sed 's/\s\+$//;/^$/d' \
    > "$f"
  fi
done

