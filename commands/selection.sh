#!/usr/bin/env bash

for dir in $(find . -type d)
do
  if [ $(ls -l "$dir" | grep '\.jpg$' | wc -l) -ge 3 ]
  then
    cp -r $dir ../slfw
  fi
done