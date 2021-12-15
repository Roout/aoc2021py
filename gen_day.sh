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

echo "The last day was $last"

next_day=$((last + 1))
echo "Create files for the day $next_day" 

echo > "src/day$next_day.py"
echo > "input/day$next_day.txt"