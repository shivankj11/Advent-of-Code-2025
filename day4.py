from helpers import *

with open('input4.txt', 'r') as f:
    text = f.read()

grid = npa(lmap(list, text.splitlines()))

ct = 0
bounds = arr_bounds(grid)
for pt in bounds:
    if grid[pt] != '@':
        continue
    neighbor_papers = sum(
        n_pt in bounds and grid[n_pt] == '@' for n_pt in grid_neighbors(pt, diagonals=True)
    )
    if neighbor_papers < 4:
        ct += 1

print('Part 1:', ct)


ncts = {}
for pt in bounds:
    if grid[pt] == '@':
        neighbor_papers = sum(
            n_pt in bounds and grid[n_pt] == '@' for n_pt in grid_neighbors(pt, diagonals=True)
        )
        ncts[pt] = neighbor_papers

removed = True
removed_ct = 0
while removed:
    removed = False
    for pt in bounds:
        if ncts.get(pt, 5) < 4:
            removed = True
            ncts.pop(pt)
            removed_ct += 1
            grid[pt] = '.'
            for n_pt in grid_neighbors(pt, diagonals=True):
                if n_pt in bounds and grid[n_pt] == '@':
                    ncts[n_pt] -= 1

print('Part 2:', removed_ct)
