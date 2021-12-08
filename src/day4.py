
def check_row_winner(matrix, used):
    for row in range(0, len(matrix)):
        is_win = True
        for v in matrix[row]:
            if v not in used:
                is_win = False
                break
        if is_win:
            return row
    return None

def check_col_winner(matrix, used):
    size = len(matrix)
    for col in range(0, size):
        is_win = True
        for row in range(0, size):
            if matrix[row][col] not in used:
                is_win = False
                break
        if is_win:
            return col
    return None
            
def sum_not_used(matrix, used):
    s = 0
    for r in matrix:
        for c in r:
            if c not in used:
                s += c
    return s

def part_1(values, matricies):
    used = set()
    for x in values:
        used.add(x)
        for index in range(0, len(matricies)):
            res = check_row_winner(matricies[index], used)
            if res != None:
                return x * sum_not_used(matricies[index], used)
            res = check_col_winner(matricies[index], used)
            if res != None:
                return x * sum_not_used(matricies[index], used)
    return None

def part_2(values, matricies):
    used = set()
    winners = set()
    for x in values:
        used.add(x)
        last_winner = 0
        for index in range(0, len(matricies)):
            if index in winners: 
                continue
            res = check_row_winner(matricies[index], used)
            if res != None:
                winners.add(index)
                last_winner = index
            res = check_col_winner(matricies[index], used)
            if res != None:
                winners.add(index)
                last_winner = index
        if len(winners) == len(matricies):
            return x * sum_not_used(matricies[last_winner], used)
    return None

values = []
with open('../input/day4.txt', 'r') as istream:
    values = [ int(x) for x in istream.readline().split(',')]
    # skip line
    istream.readline()

    matricies = []
    index = 0
    acc = []
    for line in istream:
        line = line.strip(' \n')
        if len(line) == 0: 
            if len(acc) > 0:
                matricies.append(acc.copy())
                acc.clear()
                index += 1
            continue
        acc.append([int(x) for x in line.split() ])

    print("Part 1: ", part_1(values, matricies))
    print("Part 2: ", part_2(values, matricies))
    
