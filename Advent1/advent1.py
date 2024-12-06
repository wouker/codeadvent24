input_file = './Advent1/input2'


def calc_distance():
    values_left, values_right = read_input()

    total_distance = 0
    index = 0
    for left_val in values_left:
        right_val = values_right[index]
        distance = abs(left_val - right_val)
        print(f'{index=} {left_val=} {right_val=} {distance=}')
        total_distance += distance
        index += 1

    return total_distance


def calc_similarity():
    values_left, values_right = read_input()

    total_similarity = 0
    for left_val in values_left:
        occurrence = values_right.count(left_val)
        similarity = left_val * occurrence
        print(f'{left_val=} {occurrence=} {similarity=}')
        total_similarity += similarity
    return total_similarity


def read_input():
    values_left = []
    values_right = []
    with open(input_file) as file:
        while line := file.readline():
            line_values = line.split()
            values_left.append(int(line_values[0]))
            values_right.append(int(line_values[1]))

    values_left.sort()
    values_right.sort()
    return values_left, values_right
