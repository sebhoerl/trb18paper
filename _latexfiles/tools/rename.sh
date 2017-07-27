#!/bin/sh

case $(uname -s) in
  Darwin | FreeBSD) sed_i="-i ''";;
  *)                sed_i="-i";;
esac

old_name=$1
new_name=$2

if [ -z "$old_name" -o -z "$new_name" ]; then
  echo "Usage: $0 old-name new-name" >> /dev/stderr
  exit 1
fi

find . -maxdepth 1 -type f -exec sed $sed_i "s/$old_name/$new_name/g" \{\} \+
mmv "$old_name.*" "$new_name.#1"
