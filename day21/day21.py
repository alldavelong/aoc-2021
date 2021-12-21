#!/usr/bin/env python3

import re

file = open('input.txt')
# file = open('test.txt')
input = file.read().splitlines()
file.close()

class Player:
    def __init__(self, starting_pos) -> None:
        self.starting_pos = starting_pos
        self.position = starting_pos
        self.score = 0

    def __increase_score(self, increment:int) -> int:
        self.score += increment
        return self.score

    def move_to(self, destination:int) -> int:
        """set the new player's position and increase the score by the value of the destination, returns the new score"""
        self.position = destination
        self.__increase_score(destination)
        return self.score

    @staticmethod
    def read_player_description(description_string:str) -> int:
        """reads the player description string and returns the int value of the player's starting position"""
        numbers = re.match('^Player \d* starting position: (\d*)$', description_string)
        return int(numbers.group(1))

class Die:
    def __init__(self,sides) -> None:
        self.sides = sides
    def roll(self, number_of_times=1) -> int:
        pass

class DeterministicDie(Die):
    def __init__(self, sides) -> None:
        super().__init__(sides)
        self.previous_value = 0
        self.roll_count = 0

    def roll(self, number_of_times=1) -> int:
        sum = 0
        for i in range(number_of_times):
            self.previous_value = self.previous_value + 1 if self.previous_value < self.sides else 1
            sum += self.previous_value
        self.roll_count += number_of_times
        return sum

class Game:
    def __init__(self, player_starting_positions:list[int], die:Die, board_size:int, die_rolls_per_move=1) -> None:
        self.players = [Player(pos) for pos in player_starting_positions]
        self.die = die
        self.board_size = board_size
        self.die_rolls_per_move = die_rolls_per_move

    def __calculate_new_player_position(self, player_index, steps_to_go:int) -> int:
        destination = (self.players[player_index].position + steps_to_go) % self.board_size
        return destination if destination > 0 else self.board_size

    def __move(self, player_index):
        """rolls the die, moves the player"""
        move_fields = self.die.roll(self.die_rolls_per_move)
        new_position = self.__calculate_new_player_position(player_index, move_fields)
        self.players[player_index].move_to(new_position)
        # print('player %d now at pos %d with score %d' % (player_index+1, new_position, self.players[player_index].score))

    def play(self, play_until_point_limit=1000):
        current_player = 0
        while True:
            self.__move(current_player)
            if self.players[current_player].score >= play_until_point_limit:
                break
            current_player = (current_player + 1) % len(self.players)

    def print_stats(self):
        print("="*20)
        for p, player in enumerate(self.players):
            print('player %d %s with %d points' % (p, "won" if player.score >= 1000 else "lost", player.score))
        print("="*20)

    def get_scoreboard(self) -> list[int]:
        return [p.score for p in sorted(self.players, key=lambda x: x.score, reverse=True)]

def part1():
    die = DeterministicDie(100)
    game = Game(
        [Player.read_player_description(line) for line in input],
        die,
        board_size=10,
        die_rolls_per_move=3)
    game.play()
    game.print_stats()
    loser_score = game.get_scoreboard().pop()
    print("(die rolled %d times) * (losing player score %d) = result %d" % (die.roll_count, loser_score, die.roll_count*loser_score))
    
part1()
# I didn't come up with a working solution for part2
# but William Y. Feng explains a very nice one on YouTube https://www.youtube.com/watch?v=tEPgMuqZZGE&ab_channel=WilliamY.Feng