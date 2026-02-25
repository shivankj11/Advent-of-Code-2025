from helpers import *

with open('input11.txt', 'r') as f:
    text = f.read()

text = '''svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out'''
map_lines = [line.split(': ') for line in text.splitlines()]
maps = {}
for a, b in map_lines:
    maps[a] = b.split(' ')

# Part 1
# q = ['you']
# seen = {'you' : 1}
# while q:
#     curr = q.pop(0)
#     for neighbor in maps.get(curr, []):
#         if neighbor in seen:
#             seen[neighbor] += seen[curr]
#         else:
#             seen[neighbor] = seen[curr]
#             q.append(neighbor)

# print('Part 1:', seen['out'])

# Part 2
q = ['svr']
seen = {'svr' : 1}
paths = []
while q:
    curr, visited = q.pop(0)
    for neighbor in maps.get(curr, []):
        if neighbor == 'out':
            paths.append((curr, visited | {curr}))
        if neighbor in seen:
            seen[neighbor] += seen[curr]
        else:
            seen[neighbor] = seen[curr]
            q.append((neighbor, visited | {curr}))

n_paths = 0
for from_node, path in paths:
    if 'dac' in path and 'fft' in path:
        n_paths += seen[from_node]

print('Part 2:', n_paths)