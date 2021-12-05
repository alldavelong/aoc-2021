#!/usr/bin/env python3

file = open('input.txt')
lines = file.readlines()
file.close()
inc_count = 0

def line_increase_count():
    previous = lines[0]
    for line in lines:
        if int(line) > int(previous):
            global inc_count
            inc_count += 1
        previous = line

def three_measurement_increase_count():
    # only need to compare first of A and last of B etc. because (A1, A2=B1, A3=B2, B3)
    # what's between is the same for both
    minus3 = int(lines[0])
    for i in range(3,len(lines)):
        if int(lines[i]) > minus3:
            global inc_count
            inc_count += 1
        minus3 = int(lines[i-2])

#line_increase_count()
three_measurement_increase_count()
print(inc_count)