#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
LINES = file.read().splitlines()
file.close()

MATCHING_CHARACTERS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}
ERROR_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
AUTOCOMPLETE_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

def find_wrong_character(line) -> chr:
    expected_chars = []
    for char in line:
        if char in MATCHING_CHARACTERS.keys():
            expected_chars.append(MATCHING_CHARACTERS[char])
        else:
            if char == expected_chars.pop(): continue
            else: return char
    return None

def part1():
    error_score = 0
    for line in LINES:
        error_char = find_wrong_character(line)
        if error_char != None:
            error_score += ERROR_SCORE[error_char]
    print('error score of illegal characters: %d' % error_score)

def calculate_autocomplete_score(missing_chars:list[chr]) -> int:
    score = 0
    for char in missing_chars:
        score = score * 5 + AUTOCOMPLETE_SCORE[char]
    return score

def complete_line(line) -> list[chr]:
    expected_chars = []
    missing_chars = []
    for char in line:
        if char in MATCHING_CHARACTERS.keys():
            expected_chars.append(MATCHING_CHARACTERS[char])
        else:
            next_expected = expected_chars.pop()
            if char == next_expected: continue
            else:
                missing_chars.append(char)
                expected_chars.append(next_expected)
    missing_chars.extend(expected_chars[::-1])
    return missing_chars

def part2():
    lines_without_error = [
        line
        for line in LINES
        if find_wrong_character(line) == None
    ]
    
    scores = []
    for line in lines_without_error:
        missing_chars = complete_line(line)
        score = calculate_autocomplete_score(missing_chars)
        scores.append(score)

    middle_score = sorted(scores)[int(len(scores)/2)]
    print('middle autocomplete score: %d' % middle_score)

part1()
part2()