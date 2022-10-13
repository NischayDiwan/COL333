import random
import numpy as np
from typing import List, Tuple, Dict

from connect4.utils import get_pts, get_valid_actions, Integer


class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        self._max_depth = 4

    def __new_state(self,player_num: int, move: Tuple[int,bool], state: Tuple[np.array, Dict[int, Integer]]):
        board,num_popouts=state
        new_board = np.copy(board)
        new_num_popouts = num_popouts.copy()
        column,is_popout=move
        if not is_popout:
            for row in range(new_board.shape[0]-1,-1,-1):
                if new_board[row,column]==0:
                    new_board[row,column]=player_num
                    break
        else:
            new_board[new_board.shape[0]-1,column]=0
            for row in range(new_board.shape[0]-1,0,-1):
                new_board[row,column]=new_board[row-1,column]
            new_num_popouts[player_num].decrement()
        return new_board,new_num_popouts

    def __expectimax_heuristic():
        pass

    def __expectimax_search(self,player_num: int,move: Tuple[int,bool],state: Tuple[np.array, Dict[int, Integer]],depth: int):
        new_state = self.__new_state(player_num,move,state)
        if depth >= self._max_depth:
            return get_pts(player_num,new_state[0])
        opp_moves = get_valid_actions(3-player_num,new_state)
        if depth%2 == 1:
            score = 0.0
            for mov in opp_moves:
                temp_state = self.__new_state(3-player_num,mov,new_state)
                score+=self.__expectimax_search(3-player_num,mov,temp_state,depth+1)
            if len(opp_moves)!=0:
                score/=len(opp_moves)
            return score
        else:
            score = -np.inf
            for mov in opp_moves:
                temp_state = self.__new_state(3-player_num,move,new_state)
                score = max(score,self.__expectimax_search(3-player_num,mov,temp_state,depth+1))
            return score



    def __intelligent_search(self):
        pass

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        self.__intelligent_search()

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        possible_moves = get_valid_actions(self.player_number,state)
        max_score = -np.inf
        expectimax_move = None
        for move in possible_moves:
            temp_score = self.__expectimax_search(self.player_number,move,state,0)
            if temp_score > max_score:
                max_score = temp_score
                expectimax_move = move
        return expectimax_move
