from helpers import *

with open('input6.txt', 'r') as f:
    text = f.read()

problems = npa(lmap(str.split, text.splitlines())).T

total = 0
for problem in problems:
    f = op.add if problem[-1] == '+' else op.mul
    total += reduce(f, map(int, problem[:-1]))

print('Part 1:', total)


total = 0
textL = text.splitlines()
ops_text = textL[-1]
for i in range(len(ops_text)):
    if ops_text[i] != ' ':
        j = i + 1
        while j < len(ops_text) and ops_text[j] == ' ':
            j += 1
        ns = []
        for k in range(i, j-1):
            n = ''
            for v in textL[:-1]:
                if v[k] != ' ':
                    n += v[k]
            ns.append(int(n))
    
        f = op.add if ops_text[i] == '+' else op.mul
        total += reduce(f, ns)
    
print('Part 2:', total)
