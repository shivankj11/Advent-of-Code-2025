from helpers import *
from scipy.optimize import linprog

with open('input10.txt', 'r') as f:
    text = f.read()

machines_txt = [row.split(' ') for row in text.splitlines()]
machines = []
for machine in machines_txt:
    buttons = lmap_nested(int, [v[1:-1].split(',') for v in machine[1:-1]])
    joltages = lmap(int, machine[-1][1:-1].split(','))
    machines.append((machine[0][1:-1], buttons, joltages))

# Part 1
min_presses = 0
for setting, toggles_raw, _ in machines:

    toggles = []
    for buttonL in toggles_raw:
        button = 0
        for v in buttonL:
            button += (1 << v)
        toggles.append(button)

    goal = 0
    for v in setting[::-1]:
        goal <<= 1
        goal += (v == '#')

    mask = 0
    for _ in range(len(setting)):
        mask <<= 1
        mask += 1

    seen = {0}
    q = deque([(0, 0)])
    found = False
    while not found:
        val, n = q.popleft()
        for toggle in toggles:
            new = val ^ (toggle & mask)
            if new == goal:
                min_presses += n+1
                found = True
                break
            if new not in seen:
                seen.add(new)
                q.append((new, n+1))

print('Part 1:', min_presses)

# Part 2
min_presses = 0
for _, buttons, goal in machines:

    A = npa([[1 if v in button else 0 for v in range(len(goal))]
        for button in buttons
    ]).T
    res = linprog(c=[1] * len(buttons), A_eq=A, b_eq=goal, integrality=1)
    min_presses += res.fun

print('Part 2:', min_presses)

exit()

# bf attempt
def jolt_eq(j1, j2):
    return all(v1 == v2 for v1, v2 in zip(j1, j2))

min_presses = 0
for setting, buttons, goal in machines:

    curr = [0] * len(setting)
    seen = {tuple(curr)}
    q = deque([(curr, 0)])
    found = False
    while not found:
        curr, n = q.popleft()
        for button in buttons:
            state = curr
            for v in button:
                state[v] += 1

            if jolt_eq(state, goal):
                min_presses += n+1
                found = True
                print('found1')
                break

            state_tuple = tuple(state)
            if state_tuple not in seen:
                seen.add(state_tuple)
                q.append((state, n+1))
