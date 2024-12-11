input_file = './Advent7/input1'


def calibrate():
    def process_values(current_values, value, target):
        operations = [lambda x, y: x + y, lambda x, y: x * y]
        new_values = []

        for possible_value in current_values:
            for operation in operations:
                result = operation(possible_value, value)
                if result == target:
                    return True, target, []
                elif result < target:
                    new_values.append(result)

        return False, 0, new_values

    to_check = read_input()

    valid_equations = 0
    for item in to_check:
        print(f'trying to calc {item.result} via {item.params}')

        current_possible_values = [item.params[0]]
        for param in item.params[1:]:
            found, increment, new_possible_values = process_values(current_possible_values, param, item.result)
            if found:
                print(f"{item.result} found via {item.params}")
                valid_equations += increment
                break

            current_possible_values = new_possible_values

    return valid_equations


def read_input():
    values = []
    with open(input_file) as file:
        while line := file.readline():
            line_values = line.strip().split(':')
            result = int(line_values[0])
            params = list(map(int, line_values[1].split()))
            values.append(CalibrationInput(result, params))

    return values


class CalibrationInput:
    def __init__(self, result, params):
        self.result = result
        self.params = params
