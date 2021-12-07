if [ "$#" -ne 2 ]; then
    echo "Illegal number of parameters"
    echo "Usage $0 <session_cookie> <day>"
    exit 1 
fi

AOC_SESSION=$1
DAY=$2
URL="https://adventofcode.com/2021/day/$DAY/input"

echo "Advent of code session: $AOC_SESSION"
echo "Advent of code day: $DAY"

curl --cookie "session=$AOC_SESSION" $URL > "input/day$DAY.txt"