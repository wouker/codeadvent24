input_file = './Advent2/input2'


def calc_safety():
    lines = read_input()
    safe_count = 0
    for line_values in lines:
        if len(line_values) == 0:
            continue
        if is_safe_with_toleration(line_values):
            safe_count += 1
    return safe_count


def is_safe(line_values):
    is_increase = False
    is_decrease = False
    prev_value = None
    for value in line_values:
        i_value = int(value)
        if prev_value is not None:
            if i_value < prev_value:
                is_decrease = True
            elif i_value > prev_value:
                is_increase = True
            else:
                return False

            if is_increase & is_decrease:
                return False

            if abs(prev_value - i_value) > 3:
                return False

        prev_value = i_value
    return True


def is_safe_with_toleration(line_values):
    if is_safe(line_values):
        return True

    permutations = []
    for i in range(len(line_values)):
        excluded = remove_item_by_index(line_values, i)
        permutations.append(excluded)

    for permutation in permutations:
        if is_safe(permutation):
            return True

    return False


def read_input():
    values = [[]]
    with open(input_file) as file:
        while line := file.readline():
            line_values = line.split()
            values.append(line_values)

    return values


def remove_item_by_index(original_list, index):
    return original_list[:index] + original_list[index + 1:]
