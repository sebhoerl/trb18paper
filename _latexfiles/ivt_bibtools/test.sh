#!/bin/sh

cd $(dirname $0)
FILES=$*
if [ -z "$FILES" ]
then
    FILES=*.py
fi

for F in $FILES
do
    for PYTHONVER in 2 3
    do
        echo $F | sed -r 's/\.py$//;s/^/python'$PYTHONVER' -m ivt_bibtools./'
    done
done | (cd ..; parallel --gnu && echo "ALL TESTS SUCCEEDED") || echo "$? FALED TEST(s)"

