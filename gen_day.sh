#!/bin/bash

days=($(ls "src/"))
let last=0
for i in "${days[@]}"
do
    num=$(echo "$i" | sed 's/[^0-9]/''/g')
    if (($num > $last)); then
        last=$num
    fi
done 

next_day=$((last + 1))

echo " - create src/day$next_day.py"
sed "s/{placeholder}/day$next_day.txt/g" "template.txt" > "src/day$next_day.py"

echo " - create input/day$next_day.txt"
touch "input/day$next_day.txt"