import copy
import datetime
import math
import random
from typing import List

import game_parameters
from components import Stone, Hole, Store
from decision_tree import DecisionNode, print_tree, create_decision_tree
from min_max import min_max
from player import Player


class Game:

    def __init__(self):

        self.__holes = {}
        self.__stones = []

        self.__players: List[Player] = []
        self.__active_player: int = 0

        self.__extra_move = False
        #self.__end_of_game = False

    @property
    def holes(self):
        return self.__holes

    @holes.setter
    def holes(self, holes):
        self.__holes = holes

    @property
    def stones(self):
        return self.__stones

    @stones.setter
    def stones(self, stones):
        self.__stones = stones

    @property
    def players(self):
        return self.__players

    @players.setter
    def players(self, players):
        self.__players = players

    @property
    def active_player(self):
        return self.__active_player

    @active_player.setter
    def active_player(self, active_player):
        self.__active_player = active_player

    @property
    def extra_move(self):
        return self.__extra_move

    @extra_move.setter
    def extra_move(self, extra_move):
        self.__extra_move = extra_move

    # @property
    # def end_of_game(self):
    #     return self.__end_of_game
    #
    # @end_of_game.setter
    # def end_of_game(self, end_of_game):
    #     self.__end_of_game = end_of_game

    def play(self):
        self.create_players()
        self.create_game_structure()
        self.draw_first_player()
        best_number = math.inf

        while not self.check_end_of_game():
            self.print_mancala()
            print("------------------------------------------------------")

            if not self.players[self.active_player].ai: # if not AI
                if best_number in self.get_not_empty_player_holes(self.active_player):
                    print("Best move for ", self.players[self.active_player].nick, " now:", best_number)
                hole_number = int(self.get_player_move())
                while hole_number not in self.get_not_empty_player_holes(self.active_player):
                    print("Incorrect value!")
                    hole_number = int(self.get_player_move())

            else: # AI
                if best_number in self.get_not_empty_player_holes(self.active_player):
                    hole_number = best_number
                else:
                    hole_number = random.choice(self.get_not_empty_player_holes(self.active_player))
                print(self.players[self.active_player].nick + '\'s move:', hole_number)

            self.extra_move = False
            self.make_move(hole_number)
            if self.players[self.active_player].ai:
                self.players[self.active_player].moves += 1

            if not self.extra_move:
                self.change_active_player()

            if not self.check_end_of_game():
                start_time = datetime.datetime.now()
                node = DecisionNode(self, self.active_player, hole_number)
                create_decision_tree(game_parameters.DEPTH, node)
                min_max(node, game_parameters.DEPTH, self.active_player)
                #print_tree(node)
                best_number = max(node.children, key=lambda c: c.value).number
                end_time = datetime.datetime.now()
                time_diff = (end_time - start_time)
                execution_time = time_diff.total_seconds() * 1000
                self.players[self.active_player].time += execution_time

        self.print_mancala()
        self.get_result()

    def create_players(self):
        print("Hello Player 1! Enter your nick:")
        nick = input("> ")
        print("Do you want AI to play for you? [y/n]")
        inp = input("> ")
        if inp in ["y", "Y"]:
            ai = True
        elif inp in ['n', "N"]:
            ai = False
        player1 = Player(0, nick, ai)
        print("Hello Player 2! Enter your nick:")
        nick = input("> ")
        print("Do you want AI to play for you? [y/n]")
        inp = input("> ")
        if inp in ["y", "Y"]:
            ai = True
        elif inp in ['n', "N"]:
            ai = False
        player2 = Player(1, nick, ai)
        self.players = [player1, player2]

    def create_game_structure(self):
        for player in self.players:
            for hole_number in range(1, game_parameters.HOLES_NUMBER_ROW + 1):
                stones_in_hole = []
                for color in game_parameters.COLORS:
                    stone = Stone(color)
                    stones_in_hole.append(stone)
                    self.stones.append(stone)
                hole = Hole(hole_number, player, stones_in_hole)
                self.holes[(game_parameters.HOLES_NUMBER_ROW+1) * player.player_id + hole_number] = hole
            # add store hole for each player
            self.holes[(game_parameters.HOLES_NUMBER_ROW+1) * (player.player_id+1)] = Store(player, [])

    def draw_first_player(self):
        self.active_player = k = random.randint(0, 1)

    def print_mancala(self):
        print("\t\t\tPLAYER 1: " + self.players[0].nick)
        print("\t\t", end='')
        for x in range(0, game_parameters.HOLES_NUMBER_ROW):
            print("[" + str(game_parameters.HOLES_NUMBER_ROW - x) + "] ", end='')
        print()
        print("\t\t", end='')
        for hole in reversed(self.get_player_holes(0)):
            print(" " + str(len(hole.stones)) + "  ", end='')
        print()
        print("-" + str(len(self.get_store(0).stones)) + "-\t\t\t\t\t\t\t\t\t-" + str(len(self.get_store(1).stones)) + "-")

        print("\t\t", end='')
        for hole in self.get_player_holes(1):
            print(" " + str(len(hole.stones)) + "  ", end='')
        print()
        print("\t\t", end='')
        for x in range(1, game_parameters.HOLES_NUMBER_ROW+1):
            print("[" + str(x) + "] ", end='')
        print()
        print("\t\t\tPLAYER 2: " + self.players[1].nick)

    def get_player_move(self) -> int:
        player = self.players[self.active_player]
        print(player.nick + '\'s move:')
        print("Choose hole number!")
        selected_hole = input("> ")

        return selected_hole

    def make_move(self, hole_number):
        hole = None
        for h in self.holes.values():
            if h.number == hole_number and h.player.player_id == self.active_player:
                hole = h
                break

        stones: List[Stone] = copy.copy(hole.stones)
        hole.remove_stones()

        while len(stones) > 0:
            stone = stones[0]
            hole = self.get_next_hole(hole)
            if not (isinstance(hole, Store) and hole.player.player_id == self.get_opponent_id(self.active_player)): #if it's not opponent's store
                empty = len(hole.stones) == 0 # empty before add
                stones.remove(stone)
                hole.add_stone(stone)

                if len(stones) == 0: # last stone
                    if hole == self.get_store(self.active_player): # it's player's store
                        self.extra_move = True
                    elif hole.player.player_id == self.active_player and empty and not isinstance(hole, Store): #stealing
                        opposite = self.get_opposite_hole(hole)
                        if len(opposite.stones) > 0:
                            self.steal_opponent_stones(hole, opposite)

    def steal_opponent_stones(self, hole, opposite_hole):
        store = self.get_store(self.active_player)

        store.add_all_stones(copy.copy(hole.stones))
        hole.remove_stones()
        store.add_all_stones(copy.copy(opposite_hole.stones))
        opposite_hole.remove_stones()

    def change_active_player(self):
        self.active_player = 1 - self.active_player

    def empty_holes(self, player_id):
        for hole in self.get_player_holes(player_id):
            if len(hole.stones) > 0:
                return False
        return True

    def player_stones_to_store(self, player_id):
        player_store = self.get_store(player_id)

        for hole in self.get_player_holes(player_id):
            if len(hole.stones) > 0:
                player_store.add_all_stones(copy.copy(hole.stones))
                hole.remove_stones()

    def check_end_of_game(self) -> bool:
        if self.empty_holes(self.active_player):
            self.player_stones_to_store(self.get_opponent_id(self.active_player))
            return True

        return False

    def get_winner(self):
        score_1 = self.get_points(0)
        score_2 = self.get_points(1)

        if score_1 > score_2:
            return self.players[0]
        else:
            return self.players[1]

    def get_result(self):
        winner = self.get_winner()
        print("THE WINNER IS: " + winner.nick + " CONGRATULATIONS!")
        if winner.ai:
            print("MOVES", winner.moves)
            print("TIME IN MS:", winner.time)

    def get_points(self, player_id):
        return self.get_store(player_id).count_points()

    def get_hole_global_number(self, hole) -> int:
        return (game_parameters.HOLES_NUMBER_ROW+1) * hole.player.player_id + hole.number

    def get_opposite_hole(self, hole) -> Hole:
        return self.holes[14 - self.get_hole_global_number(hole)]

    def get_next_hole(self, hole) -> Hole:
        next_hole_number = (self.get_hole_global_number(hole) + 1) % game_parameters.HOLES_NUMBER_TOTAL
        if next_hole_number == 0:
            next_hole_number = game_parameters.HOLES_NUMBER_TOTAL
        return self.holes[next_hole_number]

    def get_player_hole_numbers(self, player_id) -> List[int]:
        start_range = (game_parameters.HOLES_NUMBER_ROW + 1) * player_id + 1
        return list(range(start_range, start_range + game_parameters.HOLES_NUMBER_ROW))

    def get_player_holes(self, playes_id) -> List[Hole]:
        holes = []
        holes_numbers = self.get_player_hole_numbers(playes_id)
        for number, hole in self.holes.items():
            if number in holes_numbers:
                holes.append(hole)

        return holes

    def get_store(self, player_id) -> Store:
        return self.holes[(game_parameters.HOLES_NUMBER_ROW+1) * (player_id+1)]

    def get_opponent_id(self, player_id) -> int:
        return 1 - player_id

    def get_not_empty_player_holes(self, player_id) -> List[int]:
        holes = self.get_player_holes(player_id)
        not_empty = []
        for hole in holes:
            if len(hole.stones) > 0:
                not_empty.append(hole.number)

        return not_empty















