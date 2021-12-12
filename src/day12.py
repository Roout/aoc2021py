

def dfs_1(adj:dict, big:set, vert:str, used: set):
    assert(vert in adj)
    
    if vert == 'end':
        return 1
    ans = 0
    for to in adj[vert]:
        if to not in used:
            if to not in big:
                used.add(to)
            ans += dfs_1(adj, big, to, used)
            if to not in big:
                used.remove(to)
    return ans

def can_visit(visits: dict, big: set, vert: str, twice: dict):
    if vert in big:
        return True
    if vert not in visits:
        return True
    if vert == 'start':
        return False
    limit = 2 if vert in twice else 1
    return visits[vert] < limit

def visit(visits: dict, big: set, vert: str, twice: dict):
    if vert in big:
        return

    if vert in visits:
        visits[vert] += 1
    else:
        visits[vert] = 1

    if vert in twice:
        twice[vert] += 1

def leave(visits: dict, big: set, vert: str, twice: dict):
    if vert in big:
        return
    if vert in twice:
        twice[vert] -= 1
    visits[vert] -= 1

def dfs_2(adj:dict, big:set, vert:str, visits: dict, path: list, twice: dict):
    assert(vert in adj)

    if vert == 'end':
        if next(iter(twice.values())) == 2:
            return 1
        return 0
    ans = 0
    for to in adj[vert]:
        if can_visit(visits, big, to, twice):
            visit(visits, big, to, twice)
            path += [to]
            ans += dfs_2(adj, big, to, visits, path, twice)
            path.pop()
            leave(visits, big, to, twice)
    return ans


def part_1(adj, big):
    used = {'start'}
    return dfs_1(adj, big, 'start', used)

def part_2(adj, big):
    visits = { 'start': 1 }
    s = 0
    for (v, l) in adj.items():
        if v not in big and v != 'start' and v != 'end':
            s += dfs_2(adj, big, 'start', visits, ['start'], {v: 0})
    return s

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

# without repeated small caves
print('Part_1: ', part_1(adj, big)) 
# use only pathes with 1 small cave + use only pathes with 2 small caves
print('Part_2: ', part_1(adj, big) + part_2(adj, big))