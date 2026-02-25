from helpers import *

with open('input7.txt', 'r') as f:
    text = f.read()

grid = npa(lmap(list, text.splitlines()))

start = find(grid, 'S', first=True)

def add_unseen(pt, q, seen):
    if pt not in seen:
        seen.add(pt)
        q.append(pt)

q = [start]
ct = 0
seen = {start}
while q:
    x, y = q.pop(0)
    if x == grid.shape[0] - 1:
        continue
    if grid[x+1, y] == '^':
        add_unseen((x+1, y-1), q, seen)
        add_unseen((x+1, y+1), q, seen)
        ct += 1
    else:
        add_unseen((x+1, y), q, seen)

print("Part 1:", ct)


q = [start]
seen = {start}
cts = defaultdict(int)
cts[start] = 1
while q:
    x, y = q.pop(0)
    if x == grid.shape[0] - 1:
        continue
    if grid[x+1, y] == '^':
        left, right = (x+1, y-1), (x+1, y+1)
        add_unseen(left, q, seen)
        cts[left] += cts[(x, y)]
        add_unseen(right, q, seen)
        cts[right] += cts[(x, y)]
    else:
        add_unseen((x+1, y), q, seen)
        cts[(x+1, y)] += cts[(x, y)]

print("Part 2:", sum(cts[x, y] for x,y in cts if x == grid.shape[0] - 1))
