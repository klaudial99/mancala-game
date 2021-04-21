from typing import List


class Stone:

    def __init__(self, color):
        self.__color: str = color

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color


class Hole:

    def __init__(self, number, player, stones):
        self.__number: int = number
        self.__player = player
        self.__stones: List[Stone] = stones

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        self.__number = number

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, player):
        self.__player = player

    @property
    def stones(self):
        return self.__stones

    @stones.setter
    def stones(self, stones):
        self.__stones = stones

    def remove_stones(self):
        self.stones.clear()

    def add_stone(self, stone: Stone):
        self.stones.append(stone)


class Store(Hole):

    def __init__(self, player, stones):
        super().__init__(7, player, stones)

    def add_all_stones(self, stones: List[Stone]):
        self.stones.extend(stones)

    def count_points(self):
        return len(self.stones)
