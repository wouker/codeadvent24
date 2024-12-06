from enum import IntEnum

input_file = './Advent4/input2'


class Offset(IntEnum):
    ZERO = 0
    POSITIVE = 1
    NEGATIVE = -1


class Direction:
    def __init__(self, name: str, row_move: Offset, column_move: Offset):
        self.name = name
        self.row_move = row_move
        self.column_move = column_move

    def __repr__(self):
        return f"Direction(name='{self.name}', row_move={self.row_move}, column_move={self.column_move})"


class CrossFindLeg:
    def __init__(self, direction: Direction, ix_row: int, ix_col: int):
        self.direction = direction
        self.ix_row = ix_row
        self.ix_col = ix_col

    def __repr__(self):
        return f"CrossFindLeg({self.direction=}, {self.ix_row=}, {self.ix_col=})"


class Advent4P2(object):
    right_down = Direction("right_down", Offset.POSITIVE, Offset.POSITIVE)
    left_down = Direction("left_down", Offset.POSITIVE, Offset.NEGATIVE)
    right_up = Direction("right_up", Offset.NEGATIVE, Offset.POSITIVE)
    left_up = Direction("left_up", Offset.NEGATIVE, Offset.NEGATIVE)

    def __init__(self):
        self.start_directions = [
            self.right_down,
            self.left_down,
            self.right_up
            # left-up is no start-direction, only used when searching other leg of the X
        ]
        self.row_count = 0
        self.column_count = 0
        self.keyword = 'MAS'
        # -1 as we already have the first letter on given position
        self.max_offset = len(self.keyword) - 1
        print(f'{self.keyword=} {self.max_offset=}')

    def count_mas(self):
        print(f'** start looking for crossing {self.keyword} in matrix...')
        matrix = self.read_input()
        cross_mas_found = 0
        self.row_count = len(matrix)
        self.column_count = len(matrix[0])
        print(f'{self.row_count=} {self.column_count=}')
        for ix_row in range(self.row_count):
            row = matrix[ix_row]
            print(f'{ix_row=} {row=}')
            for ix_col in range(self.column_count):
                found_directions = self.find_mas_in_directions(ix_row, ix_col, self.start_directions, matrix)
                mas_found_in_n_directions = len(found_directions)
                # better (hindsight): to have built this around A because an A can only belong to 1 cross, an M up to 4
                if mas_found_in_n_directions > 0:
                    for found_direction in found_directions:
                        # print(f'start looking for matching {self.keyword} in cross')
                        possible_legs = self.get_cross_directions(found_direction, ix_row, ix_col)
                        cross_found = False
                        for possible_leg in possible_legs:
                            if self.find_mas_in_direction(possible_leg.ix_row, possible_leg.ix_col,
                                                          possible_leg.direction, matrix, True):
                                cross_found = True
                                print(f'!found cross {self.keyword} in {ix_row=} {ix_col=} '
                                      f'and {possible_leg.ix_row= } {possible_leg.ix_col=}')
                                cross_mas_found += 1
                                break
                        if not cross_found:
                            print(f'no cross found for {ix_row=} {ix_col=}')

        return cross_mas_found

    def find_mas_in_directions(self, ix_row, ix_col, directions, matrix):
        directions_with_mas = []
        if self.value_is_start_letter(ix_row, ix_col, matrix):
            for direction in directions:
                if self.find_mas_in_direction(ix_row, ix_col, direction, matrix):
                    directions_with_mas.append(direction)
        return directions_with_mas

    def find_mas_in_direction(self, ix_row, ix_col, direction, matrix, check_start_letter=False):
        if not check_start_letter or self.value_is_start_letter(ix_row, ix_col, matrix):
            if self.can_move_in_direction(ix_row, ix_col, direction):
                if self.find_mas(ix_row, ix_col, direction, matrix):
                    return True
        return False

    def value_is_start_letter(self, ix_row, ix_col, matrix):
        value = matrix[ix_row][ix_col]
        expected_letter = self.keyword[0]
        return value == expected_letter

    def get_cross_directions(self, init_direction, ix_row, ix_col):

        cross_move_right_go_left_down = CrossFindLeg(self.left_down, ix_row, ix_col + self.max_offset)
        cross_move_down_go_right_up = CrossFindLeg(self.right_up, ix_row + self.max_offset, ix_col)
        cross_move_down_go_left_up = CrossFindLeg(self.left_up, ix_row + self.max_offset, ix_col)
        cross_move_right_go_left_up = CrossFindLeg(self.left_up, ix_row, ix_col + self.max_offset)

        match init_direction:
            case self.right_down:
                return [cross_move_right_go_left_down, cross_move_down_go_right_up]
            case self.left_down:
                return [cross_move_down_go_left_up]
            case self.right_up:
                return [cross_move_right_go_left_up]
            case _:
                return []

    def can_move_in_direction(self, ix_row, ix_col, desired_direction):
        row_move = ix_row + (int(desired_direction.row_move) * self.max_offset)
        column_move = ix_col + (int(desired_direction.column_move) * self.max_offset)
        return 0 <= column_move < self.column_count and 0 <= row_move < self.row_count

    def find_mas(self, ix_row, ix_col, direction, matrix):
        for i in range(self.max_offset + 1):
            new_ix_row, new_ix_col = self.calc_new_point(ix_row, ix_col, direction, i)
            new_value = matrix[new_ix_row][new_ix_col]
            expected_value = self.keyword[i]
            if new_value != expected_value:
                return False

        print(f'{self.keyword} found in {direction.name} starting on {ix_row=} {ix_col=}')
        return True

    @classmethod
    def calc_new_point(cls, ix_row, ix_col, direction, offset_count):
        new_ix_row = cls.calc_offset(ix_row, direction.row_move, offset_count)
        new_ix_col = cls.calc_offset(ix_col, direction.column_move, offset_count)
        return new_ix_row, new_ix_col

    @classmethod
    def calc_offset(cls, ix, offset, offset_count):
        new_ix = ix
        match offset:
            case Offset.POSITIVE:
                new_ix += offset_count
            case Offset.NEGATIVE:
                new_ix -= offset_count
        return new_ix

    @staticmethod
    def read_input():
        values = []
        with open(input_file) as file:
            while line := file.readline():
                line_values = list(line.strip())
                values.append(line_values)

        return values


class Advent4P1(object):

    def __init__(self):
        self.directions = [
            Direction("right", Offset.ZERO, Offset.POSITIVE),
            Direction("right_down", Offset.POSITIVE, Offset.POSITIVE),
            Direction("down", Offset.POSITIVE, Offset.ZERO),
            Direction("left_down", Offset.POSITIVE, Offset.NEGATIVE),
            Direction("left", Offset.ZERO, Offset.NEGATIVE),
            Direction("left_up", Offset.NEGATIVE, Offset.NEGATIVE),
            Direction("up", Offset.NEGATIVE, Offset.ZERO),
            Direction("right_up", Offset.NEGATIVE, Offset.POSITIVE),
        ]
        self.row_count = 0
        self.column_count = 0
        self.keyword = 'XMAS'

    def count_xmas(self):
        matrix = self.read_input()
        xmas_found = 0
        self.row_count = len(matrix)
        self.column_count = len(matrix[0])
        for ix_row in range(self.row_count):
            row = matrix[ix_row]
            print(f'{ix_row=} {row=}')
            for ix_col in range(self.column_count):
                value = row[ix_col]
                if value == self.keyword[0]:
                    for direction in self.directions:
                        if self.can_move_in_direction(ix_row, ix_col, direction):
                            if self.find_xmas(ix_row, ix_col, direction, matrix):
                                xmas_found += 1

        return xmas_found

    def can_move_in_direction(self, ix_row, ix_col, desired_direction):
        row_move = ix_row + (int(desired_direction.row_move) * 3)
        column_move = ix_col + (int(desired_direction.column_move) * 3)
        return 0 <= column_move < self.column_count and 0 <= row_move < self.row_count

    def find_xmas(self, ix_row, ix_col, direction, matrix):
        # print(f'X found, searching XMAS in {direction.name=} on {ix_row=} {ix_col=}')
        for i in range(1, 4):
            new_ix_row, new_ix_col = Advent4P1.calc_new_point(ix_row, ix_col, direction, i)
            new_value = matrix[new_ix_row][new_ix_col]
            expected_value = self.keyword[i]
            if new_value != expected_value:
                return False

        print(f'XMAS found in {direction.name} starting on {ix_row=} {ix_col=}')
        return True

    @classmethod
    def calc_new_point(cls, ix_row, ix_col, direction, offset_count):
        new_ix_row = Advent4P1.calc_offset(ix_row, direction.row_move, offset_count)
        new_ix_col = Advent4P1.calc_offset(ix_col, direction.column_move, offset_count)
        return new_ix_row, new_ix_col

    @classmethod
    def calc_offset(cls, ix, offset, offset_count):
        new_ix = ix
        match offset:
            case Offset.POSITIVE:
                new_ix += offset_count
            case Offset.NEGATIVE:
                new_ix -= offset_count
        return new_ix

    @staticmethod
    def read_input():
        values = []
        with open(input_file) as file:
            while line := file.readline():
                line_values = list(line.strip())
                values.append(line_values)

        return values
