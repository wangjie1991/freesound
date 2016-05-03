#!/bin/bash

tags_file=$1
base_dir=tags

while read line
do
    dir="$base_dir/$line"
    mkdir -p "$dir"
    ./freesound.py freesound.list "$line" | xargs -J % cp % "$dir"
    #find "$dir" -name "*.txt" > temp.list
    #./freesound.py temp.list
done < $tags_file

