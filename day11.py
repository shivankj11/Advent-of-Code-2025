from helpers import *

with open('input11.txt', 'r') as f:
    text = f.read()

map_lines = [line.split(': ') for line in text.splitlines()]
maps = defaultdict(list)
for a, b in map_lines:
    maps[a] = b.split(' ')


def BFSRaw(start: str, target: str, skip: str | None=None) -> dict[str, int]:
    # visits every path
    q = [start]
    seen = defaultdict(int)
    seen[start] = 1
    while q:
        curr = q.pop(0)
        for neighbor in maps[curr]:
            seen[neighbor] += 1
            if neighbor in (skip, target):
                continue
            q.append(neighbor)
    return seen[target]


def ReachableNodes(start: str, skip: Set[str | None]) -> dict[str, int]:
    # returns all reachable nodes from start
    q = [start]
    reachable = {start}
    while q:
        curr = q.pop()
        for neighbor in maps[curr]:
            if neighbor not in reachable | skip:
                reachable.add(neighbor)
                q.append(neighbor)
    return reachable


def BFS(start: str, target: str, skip: str | None=None) -> dict[str, int]:
    # count number of reachable in-nodes for each node
    reachable = ReachableNodes(start, {target, skip})
    deps = defaultdict(int)
    for a in reachable:
        for b in maps[a]:
            deps[b] += 1
    # search from start in topo order
    q = [start]
    cts = defaultdict(int)
    cts[start] = 1
    added = {start}
    while q:
        curr = q.pop(0)
        for neighbor in maps[curr]:
            cts[neighbor] += cts[curr]
            deps[neighbor] -= 1
            if neighbor not in (skip, target, *added) and deps[neighbor] == 0:
                q.append(neighbor)
                added.add(neighbor)
    return cts[target]


# Part 1
print('Part 1:', BFS('you', 'out'))

# Part 2
# svr -> dac / fft
svr_to_dac = BFS('svr', 'dac', skip='fft')
svr_to_fft = BFS('svr', 'fft', skip='dac')
# dac / fft -> fft / dac
dac_to_fft = BFS('dac', 'fft')
fft_to_dac = BFS('fft', 'dac')
# dac / fft -> out
dac_to_out = BFS('dac', 'out', skip='fft')
fft_to_out = BFS('fft', 'out', skip='dac')
# sum up ways
svr_dac_fft_out = svr_to_dac * dac_to_fft * fft_to_out
svr_fft_dac_out = svr_to_fft * fft_to_dac * dac_to_out
print("Part 2:", svr_dac_fft_out + svr_fft_dac_out)
