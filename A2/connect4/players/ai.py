import random
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer
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
        self._max_depth = 10
        self._col_dimension = 0

    def __eval_expectimax(self,player_num: int,state: Tuple[np.array, Dict[int, Integer]],move: Tuple[int,bool]):
        x = get_pts(player_num,state[0])
        y = get_pts(3-player_num,state[0])
        c,p = move
        bc = 0.5*abs(c-self._col_dimension//2)
        e = x-y-bc
        return e

    def __eval(self,player_num: int,state: Tuple[np.array, Dict[int, Integer]],move: Tuple[int,bool]):
        x = get_pts(player_num,state[0])
        y = get_pts(3-player_num,state[0])
        if(player_num == 1):
            e = x-y
        else:
            e = x-y
        return e

    def __expectimax_search(self,player_num: int,move: Tuple[int,bool],state: Tuple[np.array, Dict[int, Integer]],depth: int):
        new_state = next_state(player_num,move,state)
        if depth >= self._max_depth:
            return self.__eval_expectimax(player_num,new_state,move)
        opp_moves = get_valid_actions(3-player_num,new_state)
        score = 0.0
        for mov in opp_moves:
            temp_state = next_state(3-player_num,mov,new_state)
            new_movs = get_valid_actions(player_num,temp_state)
            maxi_score = 0
            for new_mov in new_movs:
                new_mov_score = self.__expectimax_search(player_num,new_mov,temp_state,depth+1)
                # print("thought move at depth :",depth,new_mov, new_mov_score)
                maxi_score = max(maxi_score,new_mov_score)
            score+=maxi_score
            # print("max score i get if opp plays",mov,"at depth :",depth,maxi_score)
        if len(opp_moves)!=0:
            score/=len(opp_moves)
        return score

    def __minimax_search(self,player_num: int,move: Tuple[int,bool],state: Tuple[np.array, Dict[int, Integer]],depth: int):
        new_state = next_state(player_num,move,state)
        if depth >= self._max_depth:
            return self.__eval(player_num,new_state,move)
        opp_moves = get_valid_actions(3-player_num,new_state)
        mini_score = np.inf
        for mov in opp_moves:
            temp_state = next_state(3-player_num,mov,new_state)
            new_movs = get_valid_actions(player_num,temp_state)
            maxi_score = -np.inf
            for new_mov in new_movs:
                new_mov_score = self.__minimax_search(player_num,new_mov,temp_state,depth+1)
                # print("thought move at depth :",depth,new_mov, new_mov_score)
                maxi_score = max(maxi_score,new_mov_score)
            if len(new_movs) ==0:
                print("no moves for me")
                maxi_score = self.__eval(player_num,temp_state,mov) 
            mini_score = min(mini_score,maxi_score)
            # print("max score i get if opp plays",mov,"at depth :",depth,maxi_score)
        if len(opp_moves)==0:
            print("no moves for opponent")
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
        m = max(board.shape[1],len(possible_moves))
        self._max_depth = math.floor(math.log(self.time,m) + 0.5 * math.log(2*self.time,m))
        print(self._max_depth)   
        max_score = -np.inf
        minimax_move = possible_moves[0]
        for move in possible_moves:
            toc = time.perf_counter()
            # if(toc-tic > 9 * (self.time)/10):
            #     break
            temp_score = self.__minimax_search(self.player_number,move,state,0)
            # print("thought move at depth :",0,move, temp_score)
            if temp_score > max_score:
                max_score = temp_score
                minimax_move = move
        toc = time.perf_counter()
        print("time left :",self.time-toc+tic)
        print(self.player_number,"making move at depth :",0,minimax_move,max_score)
        return minimax_move

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
        self._col_dimension = board.shape[1]
        m = max(board.shape[1],len(possible_moves))
        self._max_depth = math.floor(math.log(self.time,m) + 0.1 * math.log(2*self.time,m))
        print(self._max_depth)   
        max_score = 0
        expectimax_move = possible_moves[0]
        for move in possible_moves:
            toc = time.perf_counter()
            if(toc-tic > 9 * (self.time)/10):
                break
            temp_score = self.__expectimax_search(self.player_number,move,state,0)
            print("thought move at depth :",0,move, temp_score)
            if temp_score > max_score:
                max_score = temp_score
                expectimax_move = move
        toc = time.perf_counter()
        print("time left :",self.time-toc+tic)
        print("making move at depth :",0,expectimax_move,max_score)
        return expectimax_move
