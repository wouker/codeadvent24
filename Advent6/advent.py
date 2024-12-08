from collections import namedtuple


input_file = './Advent6/input2'


GuardPoint = namedtuple('GuardPoint', ['r_ix', 'c_ix'])


def get_start_point(guard_map):
    for r_ix, r in enumerate(guard_map):
        for c_ix, c in enumerate(r):
            if c == '^':
                print(f'start_point {r_ix=} {c_ix=}')
                return GuardPoint(r_ix, c_ix)
    print(f'!!! No starting position found.')
    return None


def in_map(guard_point, guard_map):
    rows = len(guard_map)
    columns = len(guard_map[0])
    return 0 <= guard_point.r_ix < rows and 0 <= guard_point.c_ix < columns


def get_next_point(guard_point, current_direction):
    match current_direction:
        case 'u':
            return GuardPoint(guard_point.r_ix - 1, guard_point.c_ix)
        case 'r':
            return GuardPoint(guard_point.r_ix, guard_point.c_ix +1)
        case 'd':
            return GuardPoint(guard_point.r_ix +1, guard_point.c_ix)
        case 'l':
            return GuardPoint(guard_point.r_ix, guard_point.c_ix-1)


def turn(current_direction):
    match current_direction:
        case 'u': return 'r'
        case 'r': return 'd'
        case 'd': return 'l'
        case 'l': return 'u'


def evaluate_next_point(guard_map, current_point, next_point, current_direction):
    if in_map(next_point, guard_map) and guard_map[next_point.r_ix][next_point.c_ix] == '#':
        new_direction = turn(current_direction)
        print(f'{next_point=} on obstacle. turned to {new_direction}')
        return current_point, new_direction
    else:
        return next_point, current_direction


def calc_route():
    guard_map = read_input()
    guard_point = get_start_point(guard_map)
    current_direction = 'u'
    unique_positions = [guard_point]

    while in_map(guard_point, guard_map):
        next_point = get_next_point(guard_point, current_direction)
        guard_point, current_direction = evaluate_next_point(guard_map, guard_point, next_point, current_direction)
        if in_map(guard_point, guard_map) and guard_point not in unique_positions:
            unique_positions.append(guard_point)

    return len(unique_positions)


def calc_infinite_loops():
    guard_map = read_input()
    guard_point = get_start_point(guard_map)

    #todo https://adventofcode.com/2024/day/6
    return 0


def read_input():
    values = []
    with open(input_file) as file:
        while line := file.readline():
            line_values = list(line.strip())
            values.append(line_values)

    return values