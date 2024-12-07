import math
import functools

input_file = './Advent5/input2'


def page_in_front_is_allowed_in_front(page, page_in_front, sort_rules):
    if page in sort_rules:
        pages_belonging_after = sort_rules[page]
        return page_in_front not in pages_belonging_after
    return True


def get_middle(pages):
    middle = pages[math.floor(len(pages) / 2)]
    print(f'{middle=} for {pages=}')
    return middle

def compare(item1, item2, sort_rules):
    # we only need to check item2: if item2 is a key and key_rules and item1 exists in sort_rules, item1 should be after item 2
    if item2 in sort_rules and item1 in sort_rules[item2]:
        return 1
    return -1

def middle_pages_number():
    sort_rules, print_orders = read_input()
    sum_middle = 0
    for print_order in print_orders:
        print(f'evaluating {print_order=}')
        pages= list(map(lambda x: int(x), print_order.split(',')))
        index = 0
        valid_print_order = True
        for page in pages:
            if not valid_print_order:
                break
            pages_in_front = pages[:index]

            for page_in_front in pages_in_front:
                valid_print_order = page_in_front_is_allowed_in_front(page, page_in_front, sort_rules)
                if not valid_print_order:
                    break
            index += 1
        if not valid_print_order:
            sorted_pages = sorted(pages, key=functools.cmp_to_key(lambda page1, page2: compare(page1, page2, sort_rules)))
            print(f'{sorted_pages=}')
            sum_middle += get_middle(sorted_pages)

    return sum_middle


def read_input():
    sort_rules = {}
    orders = []
    with open(input_file) as file:
        first_part = True
        while line := file.readline():
            line = line.strip()
            if line == "":
                first_part = False
            if first_part:
                key_value = line.split('|')
                key = int(key_value[0])
                value = int(key_value[1])
                if key in sort_rules:
                    sort_rules[key].append(value)
                else:
                    sort_rules[key] = [value]
            elif line != "":
               orders.append(line)
    return sort_rules, orders
