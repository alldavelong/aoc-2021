#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
template, raw_ruleset = file.read().split('\n\n')
file.close()

class Rule:
    def __init__(self, pair:tuple, to_insert:chr) -> None:
        self.pair = pair
        self.to_insert = to_insert

    def get_new_pairs(self) -> list[str]:
        new_pairs = [
                self.pair[0] + self.to_insert,
                self.to_insert + self.pair[1]
            ]
        return new_pairs

    @staticmethod
    def i_make_the_rules(ruleset:list[str]) -> dict:
        all_rules = {}
        for rule_data in ruleset.splitlines():
            raw_pair, to_insert = rule_data.split(' -> ')
            all_rules[raw_pair] = Rule(
                tuple([char for char in raw_pair]),
                to_insert
                )
        return all_rules

    @staticmethod
    def is_pair_relevant_in_ruleset(ruleset:dict, pair:str) -> bool:
        return pair in ruleset.keys()

def find_rule_in_ruleset(ruleset:dict[str, Rule], rule_to_find:str) -> chr:
    if rule_to_find in ruleset.keys():
        # print('found: "%s" -> inserting "%c"' % (rule_to_find, ruleset[rule_to_find].to_insert))
        return ruleset[rule_to_find].to_insert
    return None
        
def update_template(input_template:str, ruleset:dict[str, Rule], update_times=1) -> str:
    if update_times == 0: return input_template
    
    updated_template = [c for c in input_template]
    for char_index in range(len(input_template)-1, 0, -1):
        find = input_template[char_index-1:char_index+1]
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
    print('Part 1:')
    ruleset = Rule.i_make_the_rules(raw_ruleset)

    updated_template = update_template(template, ruleset, 10)
    # print('length: %d of polymer %s' % (len(updated_template), updated_template))
    print('polymer length: %d' % len(updated_template))

    char_occurrences = get_char_occurrences(updated_template)
    # print(char_occurrences)

    max_count, min_count = max(char_occurrences.values()), min(char_occurrences.values())
    print('max %d - min %d = result %d' % (max_count, min_count, max_count - min_count))

def init_fast_template_update(input_template:str, ruleset:dict[str, Rule], update_times=1) -> dict:
    initial_pairs = {}
    char_count = {input_template[0]: 1}
    for char_index in range(len(input_template)-1, 0, -1):
        initial_pair = input_template[char_index-1:char_index+1]
        if Rule.is_pair_relevant_in_ruleset(ruleset, initial_pair):
            if initial_pair in initial_pairs.keys():
                initial_pairs[initial_pair] += 1
            else:
                initial_pairs[initial_pair] = 1
        
        char = input_template[char_index]
        if char in char_count.keys():
            char_count[char] += 1
        else:
            char_count[char] = 1
    return update_template_faster(initial_pairs, char_count, ruleset, update_times)

def update_template_faster(relevant_pairs:dict[str, int], char_count:dict, ruleset:dict[str, Rule], update_times) -> dict:
    if update_times == 0: return char_count
    
    new_relevant_pairs = relevant_pairs.copy()
    for pair_key in relevant_pairs.keys():
        multiplication_factor = relevant_pairs[pair_key]
        new_relevant_pairs[pair_key] -= multiplication_factor

        char_to_insert = ruleset[pair_key].to_insert
        if char_to_insert in char_count.keys():
            char_count[char_to_insert] += multiplication_factor
        else:
            char_count[char_to_insert] = multiplication_factor

        new_pairs = ruleset[pair_key].get_new_pairs()
        for add_candidate in new_pairs:
            if Rule.is_pair_relevant_in_ruleset(ruleset, add_candidate):
                if add_candidate in new_relevant_pairs.keys():
                    new_relevant_pairs[add_candidate] += multiplication_factor
                else:
                    new_relevant_pairs[add_candidate] = multiplication_factor
    return update_template_faster(new_relevant_pairs, char_count, ruleset, update_times-1)

def part2():
    print('\nPart 2:')
    # print(raw_ruleset)
    ruleset = Rule.i_make_the_rules(raw_ruleset)

    char_count = init_fast_template_update(template, ruleset, 40)
    print('character count: %s' % char_count)

    max_count, min_count = max(char_count.values()), min(char_count.values())
    print('max %d - min %d = result %d' % (max_count, min_count, max_count - min_count))

part1()
part2()