class Game:

    def __init__(self):

        self.__holes = {}
        self.__stones = []

        self.__players = []
        self.__active_player = 0

        self.__extra_move = False
        self.__end_of_game = False

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

    @property
    def end_of_game(self):
        return self.__end_of_game

    @end_of_game.setter
    def end_of_game(self, end_of_game):
        self.__end_of_game = end_of_game
