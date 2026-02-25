from helpers import *
from shapely.geometry import Polygon, box

with open('input9.txt', 'r') as f:
    text = f.read()

pts = [tuple(lmap(int, line.split(','))) for line in text.strip().splitlines()]
rectangles = [
    ((abs(a[0]-b[0])+1) * (abs((a[1]-b[1])+1)), a, b)
    for a,b in it.combinations(pts, 2)
]

# Part 1
max_area = max(rectangle[0] for rectangle in rectangles)
print('Part 1:', max_area)

# Part 2
pts.append(pts[0])
polygon = Polygon(pts)

for area, a, b in sorted(rectangles, reverse=True):
    rect = box(min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))
    if polygon.contains(rect):
        print('Part 2:', area)
        break

exit()

''' AABB overlap w rectangle x border line pairs '''
# does not work if border doubles back on itself
border = set()
pts.append(pts[0])
for pair in it.pairwise(pts):
    border.add(pair)

for area, a, b in sorted(rectangles, reverse=True):
    good = True
    for c, d in border:
        left1 = min(a[0], b[0])
        right1 = max(a[0], b[0])
        top1 = min(a[1], b[1])
        bot1 = max(a[1], b[1])
        left2 = min(c[0], d[0])
        top2 = min(c[1], d[1])
        right2 = max(c[0], d[0])
        bot2 = max(c[1], d[1])
        overlap_x = (left1 < left2 < right1) or (left1 < right2 < right1)
        overlap_y = (top1 < top2 < bot1) or (top1 < bot2 < bot1)
        if overlap_x and overlap_y:
            good = False
    
    if good:
        print('Part 2:', area)
        break

''' bf attempt '''
# would prob work with coordinate compression
border_ = set()
pts.append(pts[0])
for a,b in it.pairwise(pts):
    x1,y1 = a
    x2,y2 = b
    while (x1, y1) != (x2, y2):
        dir = (0 if y1 < y2 else
               1 if x1 < x2 else
               2 if y2 < y1 else 3)
        x1, y1 = grid_step(x1, y1, dir)
        border_.add((x1, y1))
# for attempt in grid_neighbors((x1,y1), diagonals=True)[1:]:
for attempt in [(x1+1,y1-1)]:
    border = deepcopy(border_)
    if attempt in border:
        print('skipping', attempt)
        continue
    q = [attempt]
    n = 0
    work = True
    while q:
        if n > 100000000:
            work = False
            break
        n += 1
        x, y = q.pop()
        for pt in grid_neighbors((x, y)):
            if pt not in border:
                border.add(pt)
                q.append(pt)
    if work:
        print('gottem')
        break
    else:
        print('didnt work: ', attempt)

for area, a, b in sorted(rectangles, reverse=True):
    correct = True
    for x,y in it.product(range(min(a[0], b[0]), max(a[0], b[0])), range(min(a[1], b[1]), max(a[1], b[1]))):
        if (x,y) not in border:
            correct = False
            break
    if correct:
        print('Part 2:', area)
        break
