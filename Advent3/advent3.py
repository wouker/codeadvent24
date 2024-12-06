import re

input_file = './Advent3/input2'


def multiply_cleaned_up():
    return multiply_string(read_input())


def multiply_cleaned_up_with_do():
    content = read_input()
    content = "do()"+content
    do_strings = content.split('do')
    # not foolproof if there would be substrings with do not being do() or don't() like eg. domino
    filtered_strings = [s for s in do_strings if not s.startswith("n't()")]
    sum_of_multiplications = 0
    for do_string in filtered_strings:
        sum_of_multiplications += multiply_string(do_string)
    return sum_of_multiplications


def multiply_string(content):
    matches = [tuple(map(int, match)) for match in re.findall(r"mul\((\d+),(\d+)\)", content)]
    sum_of_multiplications = 0
    for match in matches:
        product = match[0] * match[1]
        sum_of_multiplications += product
    return sum_of_multiplications


def read_input():
    with open(input_file) as file:
        return file.read()
