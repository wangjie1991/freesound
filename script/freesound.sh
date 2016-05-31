#!/bin/bash

tags_file=tags.list
data_file=data.list
base_dir=tags

while read line
do
    dir="$base_dir/$line"
    if [ ! -d "$dir" ]
    then
        mkdir -p "$dir"
    fi
    ./freesound.py "$data_file" "$line" | xargs -J % cp % "$dir"
    #find "$dir" -name "*.txt" > temp.list
    #./freesound.py temp.list
done < $tags_file

