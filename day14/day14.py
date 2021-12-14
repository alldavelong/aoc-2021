#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
template, raw_ruleset = file.read().split('\n\n')
file.close()

class Rule:
    def __init__(self, pair:tuple, to_insert:chr) -> None:
        self.pair = pair
        self.to_insert = to_insert

    @staticmethod
    def i_make_the_rules(ruleset:list[str]) -> list:
        all_rules = []
        for rule_data in ruleset.splitlines():
            raw_pair, to_insert = rule_data.split(' -> ')
            all_rules.append(Rule(
                tuple([char for char in raw_pair]),
                to_insert
                ))
        return all_rules

def find_rule_in_ruleset(ruleset:list[Rule], rule_to_find:tuple) -> chr:
    for rule in ruleset:
        if rule.pair == rule_to_find:
            # print('found: %s -> inserting "%c"' % (rule_to_find, rule.to_insert))
            return rule.to_insert
    return None
        
def update_template(input_template:str, ruleset:list[Rule], update_times=1) -> str:
    if update_times == 0: return input_template
    
    updated_template = [c for c in input_template]
    for char_index in range(len(input_template)-1, 0, -1):
        find = tuple(input_template[char_index-1:char_index+1])
        insert_char = find_rule_in_ruleset(ruleset, find)
        if insert_char != None:
            updated_template.insert(char_index, insert_char)
    # print('done %d' % update_times)
    return update_template(''.join(updated_template), ruleset, update_times-1)

def get_char_occurrences(input_string:str) -> dict:
    char_occurrences = {}
    for char in input_string:
        if char not in char_occurrences.keys():
            char_occurrences[char] = input_string.count(char)
    return char_occurrences

def part1():
    ruleset = Rule.i_make_the_rules(raw_ruleset)

    updated_template = update_template(template, ruleset, 10)
    print('len: %d of %s' % (len(updated_template), updated_template))

    char_occurrences = get_char_occurrences(updated_template)
    print(char_occurrences)

    max_count, min_count = max(char_occurrences.values()), min(char_occurrences.values())
    print('max %d - min %d = result %d' % (max_count, min_count, max_count - min_count))

def part2():
    pass

part1()
# part2()