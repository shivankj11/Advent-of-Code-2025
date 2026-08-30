from helpers import *

with open('input12.txt', 'r') as f:
    text = f.read().strip()


first = ""
second = []
for line in text.splitlines():
    if 'x' in line:
        second.append(line)
    else:
        first += line + '\n'

shapes = []
for shape_text in first.strip().split('\n\n'):
    shapes.append(npa(lmap(list, shape_text[3:].splitlines())))

trees = []
for line in second:
    dimensions, required_shapes = line.split(':')
    trees.append((lmap(int, dimensions.split('x')), lmap(int, required_shapes.split())))


""" Part 1

frame as ILP CSP: can we fit shapes into tree

actual solution that worked: # trees s.t. sum(total volume presents) <= volume of tree
"""

def orientations(shape: np.ndarray) -> List[Tuple[FrozenSet[Tuple[int, int]], int, int]]:
    """ Returns the 8 rotation x flip orientations of shape as (cells, height, width) """
    result = []
    get_cells = lambda arr: frozenset(zip(*np.where(arr == '#')))
    for _ in range(4):
        cell, cell_flip = get_cells(shape), get_cells(np.fliplr(shape))
        result.extend([(cell, *shape.shape), (cell_flip, *shape.shape)])
        shape = np.rot90(shape)
    return result

def can_fit_pysat(tree_size: Tuple[int, int], shape_counts: List[int], shapes: List[int]) -> bool:
    width, length = tree_size
    shape_areas = lmap(int, ((shape == '#').sum() for shape in shapes))
    total_shape_area = sum(lmap(lambda x: x[0] * x[1], zip(shape_areas, shape_counts)))
    if total_shape_area > width * length:
        return False

    shape_orientations = lmap(orientations, shapes)
    vpool = IDPool()
    cell_vars = defaultdict(list)
    clauses = []

    for shape_idx, count in enumerate(shape_counts):
        if count == 0:
            continue

        shape_vars = []
        for o_idx, (cells, h, w) in enumerate(set(shape_orientations[shape_idx])):
            if h > length or w > width:
                continue
            for i, j in mesh(length - h + 1, width - w + 1):
                var = vpool.id(f'P_{shape_idx}_{o_idx}_{i}_{j}')
                shape_vars.append(var)
                for dr, dc in cells:
                    cell_vars[(i+dr, j+dc)].append(var)

        if not shape_vars:
            return False

        clauses.extend(CardEnc.equals(lits=shape_vars, bound=count, vpool=vpool, encoding=EncType.seqcounter).clauses)

    for vars in cell_vars.values():
        clauses.extend(CardEnc.atmost(lits=vars, bound=1, vpool=vpool, encoding=EncType.seqcounter).clauses)

    with Glucose3(bootstrap_with=clauses) as solver:
        return solver.solve()


result = 0
for tree_size, shape_counts in trees:
    result += can_fit_pysat(tree_size, shape_counts, shapes)
    print('done 1')
print(result)

exit()

def can_fit_pulp(width: int, length: int, shape_orientations: List, shape_areas: List[int], counts: List[int]) -> bool:
    if sum(area * count for area, count in filter(lambda ac: ac[1] > 0, zip(shape_areas, counts))) > width * length:
        return False

    prob = pulp.LpProblem('fit', pulp.LpMinimize)
    cell_vars = defaultdict(list)

    for shape_idx, count in enumerate(counts):
        if count == 0:
            continue

        shape_vars = []
        for o_idx, (cells, h, w) in enumerate(set(shape_orientations[shape_idx])):
            if h > length or w > width:
                continue
            for i, j in mesh(length - h + 1, width - w + 1):
                var = pulp.LpVariable(f'P_{shape_idx}_{o_idx}_{i}_{j}', lowBound=0, upBound=count, cat='Integer')
                shape_vars.append(var)
                for dr, dc in cells:
                    cell_vars[(i+dr, j+dc)].append(var)

        if not shape_vars:
            return False

        prob += pulp.lpSum(shape_vars) == count

    for vars in cell_vars.values():
        prob += pulp.lpSum(vars) <= 1

    prob += 0
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    return pulp.LpStatus[prob.status] == 'Optimal'


# Brute force attempt
def try_add_present(shape: np.ndarray, tree: np.ndarray, start_x: int, start_y: int, rotation: int) -> Tuple[bool, Optional[np.ndarray]]:
    tree = copy.deepcopy(tree)
    rotated_shape = copy.deepcopy(shape)
    for _ in range(rotation):
        rotated_shape = np.rot90(rotated_shape)

    for x, y in it.product(range(len(rotated_shape)), range(len(rotated_shape[1]))):
        if x+start_x >= len(tree) or y+start_y >= len(tree[0]):
            return False, None
        if rotated_shape[x, y] == '#':
            if tree[x+start_x, y+start_y] == 0:
                tree[x+start_x, y+start_y] = 1
            else:
                return False, None

    return True, tree

def check_add(presents_to_add: List[int], tree: np.ndarray, current_present: int = 0, min_pos: int = 0) -> Tuple[bool, Optional[np.ndarray]]:
    if current_present == len(presents):
        return True, None

    if presents_to_add[current_present] == 0:
        return check_add(presents_to_add, tree, current_present+1, 0)

    all_positions = list(it.product(*lmap(range, (len(tree), len(tree[0]), 4))))
    for idx in range(min_pos, len(all_positions)):
        start_x, start_y, rotation = all_positions[idx]
        added, new_tree = try_add_present(shapes[current_present], tree, start_x, start_y, rotation)
        if added:
            new_presents_to_add = copy.copy(presents_to_add)
            new_presents_to_add[current_present] -= 1
            works, _ = check_add(new_presents_to_add, new_tree, current_present, idx)
            if works:
                return True, None

    return False, None

result = 0
for tree, presents in trees:
    tree_grid = np.zeros(tree)
    success, _ = check_add(presents, tree_grid)
    if success:
        result += 1