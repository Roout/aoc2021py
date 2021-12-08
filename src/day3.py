
def filter_by(values: list, cmp):
    for i in range(0, len(values[0])):
        if len(values) > 1:
            cnt = [0, 0]
            for x in values:
                cnt[0] += x[i] == '0'
                cnt[1] += x[i] == '1'
            val = cmp(cnt[0], cnt[1])
            values = list(filter(lambda item: item[i] == val, values))
        else:
            break
    return values[0]


# oxygen generator rating
# CO2 scrubber rating.
values = list()

with open('../input/day3.txt', 'r') as istream:
    for line in istream:
        values.append(line.removesuffix('\n'))

oxy = filter_by(values.copy(), lambda zeros, ones: '1' if ones >= zeros else '0')
scr = filter_by(values.copy(), lambda zeros, ones: '0' if zeros <= ones else '1')

print(int(oxy, 2) * int(scr, 2))