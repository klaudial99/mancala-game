import datetime
from time import sleep

from game import Game
from player import Player

if __name__ == '__main__':
    mancala = Game()
    mancala.play()
    # time_sum = 0
    # moves = 0
    # for x in range(10):
    #     mancala = Game()
    #     mancala.players = [Player(0, "1", True), Player(1, "2", True)]
    #     mancala.play()
    #     time_sum += mancala.get_winner().time
    #     moves = mancala.get_winner().moves
    #
    # print("TIME", time_sum/10)
    # print("MOVES", moves)