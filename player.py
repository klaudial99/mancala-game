class Player:

    def __init__(self, player_id, nick, ai):
        self.__player_id: int = player_id
        self.__nick: str = nick
        self.__points: int = 0
        self.__ai: bool = ai
        self.__time: int = 0
        self.__moves: int = 0

    @property
    def player_id(self):
        return self.__player_id

    @player_id.setter
    def player_id(self, player_id):
        self.__player_id = player_id

    @property
    def nick(self):
        return self.__nick

    @nick.setter
    def nick(self, nick):
        self.__nick = nick

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, points):
        self.__points = points

    @property
    def ai(self):
        return self.__ai

    @ai.setter
    def ai(self, ai):
        self.__ai = ai

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time

    @property
    def moves(self):
        return self.__moves

    @moves.setter
    def moves(self, moves):
        self.__moves = moves
