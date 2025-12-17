from helpers import *

with open('input1.txt', 'r') as f:
    text = f.read()

pos, ct = 50, 0
for line in text.splitlines():
    if line[0] == 'R':
        pos = (pos + int(line[1:])) % 100
    else:
        pos = (pos - int(line[1:])) % 100
    
    if pos == 0:
        ct += 1

print('Part 1:', ct)

pos, ct = 50, 0
for line in text.splitlines():
    dir, n = line[0], int(line[1:])
    ct += n // 100
    n = n % 100
    if n == 0:
        continue
    if dir == 'R':
        new_pos = (pos + n) % 100
        if new_pos == 0 or new_pos < pos:
            ct += 1
        pos = new_pos
    else:
        new_pos = (pos - n) % 100
        if new_pos == 0 or (new_pos > pos and pos != 0):
            ct += 1
        pos = new_pos
    
print('Part 2:', ct)