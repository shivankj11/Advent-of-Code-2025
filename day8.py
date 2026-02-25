from helpers import *

with open('input8.txt', 'r') as f:
    text = f.read()

pts = [tuple(map(int, p.split(','))) for p in text.strip().splitlines()]

# Part 1
distances = sorted([ # get sorted pairwise distances
    (np.sqrt(sum((a-b)**2 for a,b in zip(A,B))), A, B)
    for A, B in it.combinations(pts, 2)
])

clusters = defaultdict(int) # cluster labels after shortest 1000 connections made
n = 1
for _, A, B in distances[:1000]:
    if clusters[A] and clusters[B] and clusters[A] != clusters[B]:
        old_n = clusters[B]
        for pt in clusters:
            if clusters[pt] == old_n:
                clusters[pt] = clusters[A]
    elif clusters[A]:
        clusters[B] = clusters[A]
    elif clusters[B]:
        clusters[A] = clusters[B]
    else:
        clusters[A] = clusters[B] = n
        n += 1

cts = Counter({k : clusters[k] for k in clusters if k}.values())
print('Part 1:', reduce(op.mul, sorted(cts.values())[-3:]))

# Part 2
clusters = defaultdict(int)
n = 1
n_clusters = len(pts)
for _, A, B in distances:
    n_clusters -= 1
    if clusters[A] and clusters[B]:
        if clusters[A] != clusters[B]:
            old_n = clusters[B]
            for pt in clusters:
                if clusters[pt] == old_n:
                    clusters[pt] = clusters[A]
        else:
            n_clusters += 1
    elif clusters[A]:
        clusters[B] = clusters[A]
    elif clusters[B]:
        clusters[A] = clusters[B]
    else:
        clusters[A] = clusters[B] = n
        n += 1

    if n_clusters == 1:
        print('Part 2:', A[0] * B[0])
        break
