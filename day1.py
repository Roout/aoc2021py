
ans = 0
with open('input/day1.txt', 'r') as istream:
    prev = None
    days = [None] * 3
    for line in istream:
        if len(line) == 0: 
            break
        days = days[1:] + [None]
        days[2] = int(line)
        if days[0] != None:
            s = sum(days)
            if prev != None and s > prev: 
                ans += 1
            prev = s
print(ans)




