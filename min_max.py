import math

import game_parameters
from decision_tree import DecisionNode


def min_max(node: DecisionNode, depth, max_id, alpha=-math.inf, beta=math.inf, max_turn=True, alpha_beta=game_parameters.ALPHA_BETA):
    if depth == 0 or end_of_game(node) or node.children == []:
        node.value = measure_function(node, max_id)
        return node.value

    if max_turn:
        val = -math.inf
        max_val = -math.inf
        for child in node.children:
            is_max_turn = max_id == child.player_id
            val = max(val, min_max(child, depth-1, max_id, alpha, beta, is_max_turn, alpha_beta))
            max_val = max(max_val, val)
            if alpha_beta:
                alfa = max(alpha, val)
                if alfa >= beta:
                    break
        node.value = max_val
        return max_val
    else:
        val = math.inf
        min_val = math.inf
        for child in node.children:
            is_max_turn = max_id == child.player_id
            val = min(val, min_max(child, depth-1, max_id, alpha, beta, is_max_turn, alpha_beta))
            min_val = min(min_val, val)
            if alpha_beta:
                beta = min(beta, val)
                if beta <= alpha:
                    break
        node.value = min_val
        return min_val


def end_of_game(node: DecisionNode):
    game = node.game
    for hole in game.get_player_holes(game.active_player):
        if len(hole.stones) > 0:
            return False

    return True


def measure_function(node: DecisionNode, root_id):
    game = node.game
    return game.get_points(root_id) - game.get_points(game.get_opponent_id(root_id))

