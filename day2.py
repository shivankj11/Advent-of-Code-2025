from helpers import *

with open('input2.txt', 'r') as f:
    text = f.read()

ranges = [l.split('-') for l in text.split(',')]

tot = 0
for a,b in ranges:
    for i in range(int(a), int(b)+1):
        i_copy = i
        n_digits = 0
        while i_copy > 0:
            i_copy //= 10
            n_digits += 1
        if n_digits % 2 == 0:
            first_half = i % (10 ** (n_digits // 2))
            second_half = (i // (10 ** (n_digits // 2))) % (10 ** (n_digits // 2))
            if first_half == second_half:
                tot += i

print('Part 1:', tot)

tot = 0
for a,b in ranges:
    for i in range(int(a), int(b)+1):
        i_str = str(i)
        pattern = r'^(.+)\1+$'
        if bool(re.match(pattern, i_str)):
            tot += i

print('Part 2:', tot)
