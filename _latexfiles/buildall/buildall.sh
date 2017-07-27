#!/bin/bash

OPWD=$PWD
rm failed.log
rm succeeded.log

while read FILE
do
    echo $FILE
    BASE=`basename "$FILE"`
    if pushd "`dirname "$FILE"`";
    then
        echo $BASE
        if ! pdflatex -interaction=errorstopmode -halt-on-error "$BASE";
        then
            echo failed
            echo $FILE >> $OPWD/failed.log
            exit 1
        else
            echo succeeded
            echo $FILE >> $OPWD/succeeded.log
        fi
        popd
    else
        echo $FILE >> $OPWD/failed.log
    fi
done < listall.txt
