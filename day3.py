from helpers import *

with open('input3.txt', 'r') as f:
    text = f.read()

banks = text.splitlines()

tot_joltage = 0
for bank in banks:
    first = max(lmap(int, bank[:-1]))
    second = max(lmap(int, bank[bank.find(str(first))+1:]))
    tot_joltage += first * 10 + second

print('Part 1:', tot_joltage)


tot_joltage = 0
for bank in banks:
    n = 12
    joltage = 0
    while n > 0:
        right_pos = -n+1 if n > 1 else len(bank)
        best = max(lmap(int, bank[:right_pos]))
        best_pos = bank.find(str(best))+1
        joltage = joltage * 10 + best
        bank = bank[best_pos:]
        n -= 1
    tot_joltage += joltage

print('Part 2:', tot_joltage)