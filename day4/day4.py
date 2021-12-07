#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
datablocks = file.read().split('\n\n')
file.close()

class BingoSheet:
    """contains 5x5 matrix of Bingo guesses"""

    def __init__(self, raw_string:str):
        self.match_count = {'row': [0]*5, 'col': [0]*5}
        self.sum_of_unmatched = 0
        """total sum of all values in the BingoSheet, decreased each time a new matching value is called"""

        self.values = [[int(value) for value in line.split()] for line in raw_string.splitlines()] # form of values = [[]]*5 = [[],[],[],[],[]]
        for row in self.values:
            for value in row:
                self.sum_of_unmatched += value

    def check_new_call(self, call:int) -> bool:
        """checks if newly called value is contained
        
        :return: if this was the last needed match to win
        """
        row, col = 0, 0
        for row in range(len(self.values)):
            for col in range(len(self.values[0])):
                if self.values[row][col] == call:
                    self.sum_of_unmatched -= call
                    return self.has_won(row, col)
        return False


    def has_won(self, row:int, col:int) -> bool:
        if self.match_count['row'][row] == 4 or self.match_count['col'][col] == 4:
            return True
        else:
            self.match_count['row'][row] += 1
            self.match_count['col'][col] += 1
            return False

    @staticmethod
    def read_bingo_sheets(all_sheets:list):
        calls = [int(value) for value in all_sheets.pop(0).split(',')]
        sheets = [BingoSheet(data) for data in all_sheets]
        return calls, sheets

list_of_calls, bingo_sheets = BingoSheet.read_bingo_sheets(datablocks)

def part1():
    for call in list_of_calls:
        for sheet in bingo_sheets:
            if(sheet.check_new_call(call)):
                print('Call: %d, Sum: %d' % (call, sheet.sum_of_unmatched))
                print(call * sheet.sum_of_unmatched)
                return


def part2():
    last_removed = None
    call = 0
    while len(bingo_sheets) > 0:
        call = list_of_calls.pop(0)
        removed_at_current_call = 0
        for sheet_index in range(len(bingo_sheets)):
            if(bingo_sheets[sheet_index-removed_at_current_call].check_new_call(call)):
                last_removed = bingo_sheets.pop(sheet_index-removed_at_current_call)
                removed_at_current_call += 1
                # print('removed at call: %d  (remaining entries: %d)' % (call, len(bingo_sheets)))
    else:
        print('LAST SHEET finished at call: %d  (Sum: %d)' % (call, last_removed.sum_of_unmatched))
        print(call * last_removed.sum_of_unmatched)

# part1()
part2()
