input_file = './Advent5/input1'

def middle_pages_number():
    return 0


def read_input():
    with open(input_file) as file:
        while line := file.readline():
            #todo detect whiteline: start new logic