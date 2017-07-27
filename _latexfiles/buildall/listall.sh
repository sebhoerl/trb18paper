#!/bin/bash

grep -i '\\input{\\mypath' ../.. -lr "--include=*.tex" | grep -v '/_layouts/' > listall.txt
