import time

class Node:
    value: int
    index: int
    parent: object
    children: list

    def __init__(self, value = None, parent = None, index = None) -> None:
        self.value = value
        self.parent = parent
        self.index = index
        self.children = []

    def __str__(self) -> str:
        joined = [str(child.value) if child.value != None else '[' + str(len(child.children)) + ']' for child in self.children]
        return 'v: {}; children: {}'.format(self.value, joined)

    def __repr__(self) -> str:
        return self.__str__

    def add_child(self, value = None):
        child = Node()
        child.parent = self
        child.value = value
        child.index = len(self.children)
        self.children += [child]
        return child
    
    def is_leaf(self):
        return self.value != None
    
    def is_pair(self):
        if len(self.children) != 2:
            return False
        if self.children[0].is_leaf() and self.children[1].is_leaf():
            return True
        return False

def left_neighbour(node: Node):
    cur = node
    # bubble up
    while cur.index == 0:
        cur = cur.parent
    # it's a root
    if cur.index == None:
        return None
    cur = cur.parent.children[0]
    assert cur != None, "Congradulations! You've fucked up the logic"
    # search for most right node
    while cur.value == None:
        cur = cur.children[1]
    return cur

def right_neighbour(node: Node):
    cur = node
    # bubble up
    while cur.index == 1:
        cur = cur.parent
    # it's a root
    if cur.index == None:
        return None
    cur = cur.parent.children[1]
    assert cur != None, "Congradulations! You've fucked up the logic"
    # search for most left node
    while cur.value == None:
        cur = cur.children[0]
    return cur

def build_tree(line: str, pos: int):
    root = Node()
    cur = root
    while pos < len(line):
        if line[pos] == '[':
            child = cur.add_child()
            assert child.parent == cur
            cur = child
        elif line[pos] == ']':
            cur = cur.parent
        elif line[pos] != ',':
            assert line[pos].isdigit()
            begin = pos
            while line[pos].isdigit():
                pos += 1
            cur.add_child(int(line[begin: pos]))
            pos -= 1
        pos += 1
    return root

def explode(root: Node, depth: int):
    if root.is_pair() and depth > 4:
        left_child = left_neighbour(root)
        right_child = right_neighbour(root)
        if left_child != None:
            left_child.value += root.children[0].value
        if right_child != None:
            right_child.value += root.children[1].value
        root.children = []
        root.value = 0
        return True
    for child in root.children:
        if explode(child, depth + 1):
            return True
    return False

def split(root: Node):
    if root.is_leaf() and root.value > 9:
        root.add_child(root.value >> 1)
        root.add_child((root.value >> 1) + (root.value % 2))
        root.value = None
        return True
    for child in root.children:
        if split(child):
            return True
    return False

def stringify_tree(root: Node):
    buffer = ''
    if root.value == None:
        buffer += '['
    for n in root.children:
        if n.is_leaf():
            buffer += str(n.value)
            if n.index == 0:
                buffer += ','
        elif n.is_pair():
            buffer += '[{},{}]'.format(n.children[0].value, n.children[1].value)
            if n.index == 0:
                buffer += ','
        else:
            buffer += stringify_tree(n)
    buffer += ']'
    if root.index == 0:
        buffer += ','
    return buffer

def merge(lhs:Node, rhs:Node):
    root = Node()
    lhs.index = 0
    rhs.index = 1
    lhs.parent = root
    rhs.parent = root
    root.children = [lhs, rhs]

    reduces = None
    while reduces == None or reduces != 0:
        ops = 0
        while explode(root, 1):
            ops += 1
        if split(root):
            ops += 1
        reduces = ops 
    return root   

def magnitude(node: Node):
    if node.is_leaf():
        return node.value
    if node.is_pair():
        return 3 * node.children[0].value + 2 * node.children[1].value
    return 3 * magnitude(node.children[0]) + 2 * magnitude(node.children[1])

def part_1(snailfishes: list):
    root = build_tree(snailfishes[0], 1)
    for snail in snailfishes[1:]:
        rhs = build_tree(snail, 1)
        root = merge(root, rhs)
    return magnitude(root)

def part_2(snailfishes: list):
    count = len(snailfishes)
    highest_sum = 0
    for i in range(count):
        for j in range(i + 1, count):
            # a + b
            lhs = build_tree(snailfishes[i], 1)
            rhs = build_tree(snailfishes[j], 1)
            root = merge(lhs, rhs)
            mag = magnitude(root)
            if mag > highest_sum:
                highest_sum = mag
            # b + a    
            lhs = build_tree(snailfishes[j], 1)
            rhs = build_tree(snailfishes[i], 1)
            root = merge(lhs, rhs)
            mag = magnitude(root)
            if mag > highest_sum:
                highest_sum = mag
    return highest_sum

snailfishes = []
with open("../input/day18.txt") as istream:
    snailfishes = [line.rstrip() for line in istream]
    
begin = time.time()
print('Part_1: {}, takes {}s'.format(part_1(snailfishes), time.time() - begin))
begin = time.time()
print('Part_2: {}, takes {}s'.format(part_2(snailfishes), time.time() - begin))
