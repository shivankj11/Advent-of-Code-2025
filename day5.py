from helpers import *

with open('input5.txt', 'r') as f:
    text = f.read()

ranges, ingredients = lmap(str.splitlines, text.split('\n\n'))
ranges = lmap(lambda x : lmap(int, x.split('-')), ranges)
ingredients = lmap(int, ingredients)

ct = sum(any(a <= i <= b for a,b in ranges) for i in ingredients)

print("Part 1:", ct)


ranges.sort(key=lambda x : x[0] * (10 ** 15) + x[1])
consolidated_ranges = [ranges[0]]
for a,b in ranges[1:]:
    if a <= consolidated_ranges[-1][1]:
        consolidated_ranges[-1][1] = max(b, consolidated_ranges[-1][1])
    else:
        consolidated_ranges.append([a,b])

ct = sum(b - a + 1 for a,b in consolidated_ranges)

print("Part 2:", ct)
