import copy
from typing import List


class DecisionNode:

    def __init__(self, game, player_id, number):
        self.__game = game
        self.__player_id: int = player_id
        self.__number: int = number
        self.__value = None
        self.__children: List[DecisionNode] = []

    @property
    def game(self):
        return self.__game

    @game.setter
    def game(self, game):
        self.__game = game

    @property
    def player_id(self):
        return self.__player_id

    @player_id.setter
    def player_id(self, player_id):
        self.__player_id = player_id

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        self.__number = number

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, children):
        self.__children = children

    def add_child(self, child):
        self.children.append(child)


def create_decision_tree(depth, node: DecisionNode):
    if depth == 0:
        return

    for possible in node.game.get_not_empty_player_holes(node.player_id):
        new_game = copy.deepcopy(node.game)
        new_game.make_move(possible)
        if not new_game.extra_move:
            new_game.change_active_player()
        new_game.extra_move = False
        new_game.check_end_of_game()
        child = DecisionNode(new_game, new_game.active_player, possible)
        node.add_child(child)
        if node.game.active_player != new_game.active_player:
            create_decision_tree(depth-1, child)
        else:
            create_decision_tree(depth, child)


def print_tree(node, line="", is_last=True):
    print(line, "|--- ", f"{node.number}[{node.value}]  *next turn:{node.player_id}* ", sep="")
    line += "   " if is_last else "|  "
    child_amount = len(node.children)
    for i, child in enumerate(node.children):
        is_last = i == (child_amount - 1)
        print_tree(child, line, is_last)
