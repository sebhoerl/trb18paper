#!/bin/sh

# Sebastian Hörl
# 2017

# Use pdftotext to get word count (including references)
mkdir -p _wc
pdftotext TRB.pdf _wc/text.txt
word_count=$(cat _wc/text.txt | wc -w)
rm -r _wc

echo "\newcommand{\mytextwordcount}{$word_count}%" > mywordcount.tex
