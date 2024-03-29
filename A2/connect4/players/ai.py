import random
import numpy as np
from typing import List, Tuple, Dict, Union
from connect4.utils import get_pts, get_valid_actions, Integer
from connect4.config import win_pts
import copy
import time
import math

def next_state(player_num: int, move: Tuple[int,bool], state: Tuple[np.array, Dict[int, Integer]]):
    board,num_popouts=state
    new_board = np.copy(board)
    new_num_popouts = copy.deepcopy(num_popouts)
    column,is_popout=move
    if not is_popout:
        for row in range(new_board.shape[0]-1,-1,-1):
            if new_board[row,column]==0:
                new_board[row,column]=player_num
                break
    else:
        for row in range(new_board.shape[0]-1,0,-1):
            new_board[row,column]=new_board[row-1,column]
        new_num_popouts[player_num].decrement()
        new_board[0,column]=0
    return new_board,new_num_popouts

def get_row_score(player_number: int, row: Union[np.array, List[int]]):
    score = 0
    n = len(row)
    j = 0
    while j < n:
        if row[j] == player_number:
            count = 0
            while j < n and row[j] == player_number:
                count += 1
                j += 1
            k = len(win_pts) - 1
            score += (win_pts[count % k] ** 2) + (count // k) * (win_pts[k] ** 2)
        else:
            j += 1
    return score


def get_diagonals_primary(board: np.array) -> List[int]:
    m, n = board.shape
    for k in range(n + m - 1):
        diag = []
        for j in range(max(0, k - m + 1), min(n, k + 1)):
            i = k - j
            diag.append(board[i, j])
        yield diag


def get_diagonals_secondary(board: np.array) -> List[int]:
    m, n = board.shape
    for k in range(n + m - 1):
        diag = []
        for x in range(max(0, k - m + 1), min(n, k + 1)):
            j = n - 1 - x
            i = k - x
            diag.append(board[i][j])
        yield diag

def heuristic(player_number: int,board: np.array) -> int:
    """
    :return: Returns the total score of player (with player number) on the board
    """
    score = 0
    m, n = board.shape
    # score in rows
    for i in range(m):
        score += get_row_score(player_number, board[i])
    # score in columns
    for j in range(n):
        score += get_row_score(player_number, board[:, j])
    # scores in diagonals_primary
    for diag in get_diagonals_primary(board):
        score += get_row_score(player_number, diag)
    # scores in diagonals_secondary
    for diag in get_diagonals_secondary(board):
        score += get_row_score(player_number, diag)
    return score

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
        self._max_depth = 2
        self._col_dimension = 0

    def __eval(self,player_num: int,state: Tuple[np.array, Dict[int, Integer]],move: Tuple[int,bool]):
        x = heuristic(player_num,state[0])
        y = heuristic(3-player_num,state[0])
        return x-y

    def __minimax_search(self,player_num: int,move: Tuple[int,bool],state: Tuple[np.array, Dict[int, Integer]],depth: int, alpha: float, beta: float):
        new_state = next_state(player_num,move,state)
        if depth >= self._max_depth:
            return self.__eval(player_num,state,move)
        opp_moves = get_valid_actions(3-player_num,new_state)
        mini_score = np.inf
        for mov in opp_moves:
            temp_state = next_state(3-player_num,mov,new_state)
            new_movs = get_valid_actions(player_num,temp_state)
            maxi_score = -np.inf
            for new_mov in new_movs:
                new_mov_score = self.__minimax_search(player_num,new_mov,temp_state,depth+1,alpha,beta)
                maxi_score = max(maxi_score,new_mov_score)
                alpha = max(alpha,maxi_score)
                if maxi_score >= beta:
                    break
            if len(new_movs) ==0:
                maxi_score = self.__eval(player_num,temp_state,mov) 
            mini_score = min(mini_score,maxi_score)
            beta = min(beta,mini_score)
            if mini_score <= alpha:
                break
        if len(opp_moves)==0:
            mini_score = self.__eval(player_num,new_state,move)
        return mini_score

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
        tic = time.perf_counter()
        board,popouts=state
        possible_moves = get_valid_actions(self.player_number,state)
        self._col_dimension = board.shape[1]
        m = max(board.shape[1],len(possible_moves))
        self._max_depth = math.floor(math.log(self.time,m) + 0.5 * math.log(2*self.time,m)) +1  
        max_score = -np.inf
        minimax_move = possible_moves[0]
        for move in possible_moves:
            toc = time.perf_counter()
            # if(toc-tic > 9 * (self.time)/10):
            #     break
            temp_score = self.__minimax_search(self.player_number,move,state,0,-np.inf,np.inf)
            if temp_score > max_score:
                max_score = temp_score
                minimax_move = move
        toc = time.perf_counter()
        return minimax_move

    def __eval_expectimax(self,player_num: int,state: Tuple[np.array, Dict[int, Integer]],move: Tuple[int,bool]):
        x = heuristic(player_num,state[0])
        y = heuristic(3-player_num,state[0])
        if y!=0:
            return (x-y)/y
        else:
            return x-y

    def __expectimax_search(self,player_num: int,move: Tuple[int,bool],state: Tuple[np.array, Dict[int, Integer]],depth: int):
        new_state = next_state(player_num,move,state)
        if depth <= 0:
            return self.__eval_expectimax(player_num,new_state,move)
        opp_moves = get_valid_actions(3-player_num,new_state)
        score = 0.0
        for mov in opp_moves:
            temp_state = next_state(3-player_num,mov,new_state)
            new_movs = get_valid_actions(player_num,temp_state)
            maxi_score = -np.inf
            for new_mov in new_movs:
                new_mov_score = self.__expectimax_search(player_num,new_mov,temp_state,depth-1)
                maxi_score = max(maxi_score,new_mov_score)
            if len(new_movs) ==0:
                maxi_score = self.__eval_expectimax(player_num,temp_state,mov) 
            score+=maxi_score
        if len(opp_moves)!=0:
            score/=len(opp_moves)
        if len(opp_moves)==0:
            mini_score = self.__eval_expectimax(player_num,new_state,move)
        return score

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
        tic = time.perf_counter()
        board,popouts=state
        possible_moves = get_valid_actions(self.player_number,state)
        expectimax_move = possible_moves[0]
        for i in range(1,self._max_depth):
            toc = time.perf_counter()
            if(toc-tic > 8 * (self.time)/10):
                break
            max_score = -np.inf
            max_move = possible_moves[0]
            for move in possible_moves:
                toc = time.perf_counter()
                if(toc-tic > 9 * (self.time)/10):
                    break
                temp_score = self.__expectimax_search(self.player_number,move,state,i)            
                if temp_score > max_score:
                    max_score = temp_score
                    max_move = move
            expectimax_move = max_move
        toc = time.perf_counter()
        return expectimax_move
