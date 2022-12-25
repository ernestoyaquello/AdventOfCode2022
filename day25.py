import input
import math

PROBLEM_NUMBER = 25

def execute():
    total_decimal = 0

    for snafu_number in input.read_lines(problem_number = PROBLEM_NUMBER):
        total_decimal += from_snafu_to_decimal(snafu_number)

    return from_decimal_to_snafu(total_decimal)

def from_snafu_to_decimal(snafu_number):
    decimal_number = 0

    for index, character in enumerate(list(snafu_number)):
        position_value = pow(5, len(snafu_number) - index - 1)
        if character.isnumeric():
            decimal_number += position_value * int(character)
        elif character == '-':
            decimal_number += position_value * -1
        elif character == '=':
            decimal_number += position_value * -2

    return decimal_number

def from_decimal_to_snafu(decimal_number):
    snafu_number = ""

    position = 0
    while decimal_number != 0 or position >= 0:
        position_value = pow(5, position)
        position_amount = round(decimal_number / position_value)
        if position_amount >= 5 or position_amount <= -5:
            position += 1
        else:
            if position_amount == 4:
                snafu_number = snafu_number[:-1]
                snafu_number += '1-'
            elif position_amount == 3:
                snafu_number = snafu_number[:-1]
                snafu_number += '1='
            elif position_amount >= 0:
                snafu_number += str(position_amount)
            elif position_amount == -1:
                snafu_number += '-'
            elif position_amount == -2:
                snafu_number += '='
            elif position_amount == -3:
                snafu_number = snafu_number[:-1]
                snafu_number += '-2'
            elif position_amount == -4:
                snafu_number = snafu_number[:-1]
                snafu_number += '-1'
            decimal_number -= position_amount * position_value
            position -= 1

    return snafu_number

print("Part 1: " + str(execute()))