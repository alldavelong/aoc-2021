#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
lines = file.read().splitlines()
file.close()

word_length = len(lines[0])
line_number = len(lines)

def gamma_epsilon_count():
    one_count = [0] * word_length # = [0, 0, 0, ...]
    for line in lines:
        for i in range(0, word_length):
            if line[i] == '1':
                one_count[i] += 1
    print('ones: %s' % one_count)
    gamma = ''
    epsilon = ''
    for i in range(0, len(one_count)):
        if one_count[i] > (line_number / 2):
            gamma += '1'
            epsilon += '0'
        else:
            gamma += '0'
            epsilon += '1'
    print_decimal_product_of_two_binary_strings(gamma, epsilon)

def print_decimal_product_of_two_binary_strings(a, b):
    print('factor a: %s = %s' % (a, int(a, 2)))
    print('factor b: %s = %s' % (b, int(b, 2)))
    print(int(a, 2) * int(b, 2))

def split_list_by_bit(input_list, bit_index):
    """Sort all entries by their value at bit_index
    
    :return: two lists, one for '0's and one for '1's at bit_index
    """
    lists = [[], []]
    for line in input_list:
        if line[bit_index] == '0':
            lists[0].append(line)
        else:
            lists[1].append(line)
    return lists

def get_list_of_most_common(list, bit_index):
    lists = split_list_by_bit(list, bit_index)
    if len(lists[0]) > len(list) / 2:
        return lists[0]
    else:
        return lists[1]

def get_list_of_least_common(list, bit_index):
    lists = split_list_by_bit(list, bit_index)
    if len(lists[1]) < len(list) / 2:
        return lists[1]
    else:
        return lists[0]


def bit_criteria(list):
    bit_indices = [0,0]
    list_zero, list_one = list, list
    while list_zero == None or len(list_zero) > 1:
        list_zero = get_list_of_most_common(list_zero, bit_indices[0])
        bit_indices[0] += 1
        # print(list_zero)
    while len(list_one) > 1:
        list_one = get_list_of_least_common(list_one, bit_indices[1])
        bit_indices[1] += 1
        # print(list_one)
    print_decimal_product_of_two_binary_strings(list_zero[0], list_one[0])
    pass

# gamma_epsilon_count()
bit_criteria(lines)