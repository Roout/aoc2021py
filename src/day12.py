

def dfs(adj:dict, big:set, vert:str, used: set):
    if vert == 'end':
        return 1
    
    assert(vert in adj)

    ans = 0
    for to in adj[vert]:
        if to not in used:
            if to not in big:
                used.add(to)
            ans += dfs(adj, big, to, used)
            if to not in big:
                used.remove(to)
    return ans

def part_1(adj, big):
    used = {'start'}
    return dfs(adj, big, 'start', used)

big = set()
adj = dict()

with open('../input/day12.txt') as istream:
    for line in istream:
        (a, b) = line.rstrip('\n').split('-')
        if a == a.upper():
            big.add(a)
        if b == b.upper():
            big.add(b)

        if a not in adj:
            adj[a] = [b]
        else:
            adj[a] += [b]

        if b not in adj:
            adj[b] = [a]
        else:
            adj[b] += [a]

print('Part_1: ', part_1(adj, big))