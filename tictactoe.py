# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 09:04:45 2017

@author: Matthieu Toulemont, Ecole des Ponts 
"""

CASES = {
    "GH" : (0,0),
    "GM" : (1,0),
    "GB" : (2,0),
    "MH" : (0,1),
    "MM" : (1,1),
    "MB" : (2,1),
    "DH" : (0,2),
    "DM" : (1,2),
    "DB" : (2,2)
}

OK = [(0,0),
    (1,0),
    (2,0),
    (0,1),
    (1,1),
    (2,1),
    (0,2),
    (1,2),
    (2,2)
    ]

class Grid:
    def __init__(self):
        self._grid = [[0 for i in range(3)] for j in range(3)]
    @property
    def grid(self):
        return self._grid
    def set_case(self, i, j, var):
        self._grid[i][j] = var
    @staticmethod
    def three_in_row(row, mark):
        c = 0
        for i in range(len(row)):
            if row[i] == mark:
                c += 1
        if c == 3:
            return True
    @staticmethod
    def two_in_row(row, mark):
        c = 0
        for i in range(len(row)):
            if row[i] == mark:
                c += 1
        if c == 2:
            return True
    @staticmethod
    def one_in_row(row,mark):
        c = 0
        for i in range(len(row)):
            if row[i] == mark:
                c += 1
        if c == 1:
            return True

class Game:
    def __init__(self):
        self._grid = Grid()
        self._current_player = 0
        self._players = [0, 0]
        self._count = 0
        self._winner = 2
        self._score = [(0,0)]
        self._marks = ['O', 'X']
        self._last_move = []
        self._possible_moves = [(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2)]
    @property
    def grid(self):
        return self._grid.grid
    @property
    def current_player(self):
        return self._current_player
    @property
    def players(self):
        return self._players
    @property
    def count(self):
        return self._count
    @property
    def winner(self):
        return self._winner
    @property
    def last_move(self):
        return self._last_move
    def play(self,i,j, d):
        #print(self._score1, self._score2)
        self._last_move.append((i,j))
        if self.current_player == 0:
            self._grid.set_case(i,j,'O')

        elif self.current_player == 1:
            self._grid.set_case(i,j,'X')
        
        self.update_score()
        self.iswinner()
        # Change player
        self._current_player += 1
        self._current_player = self._current_player % 2
        
        # Update moves 
        self.update_moves()
        
        if d == "show":
            self.display()                  
    def display(self):
        grid_info = ""
        for i in range(3):
            line =""
            for j in range(3):
                line += " {} ".format(self.grid[i][j])
            grid_info += line + "\n"
        print(grid_info)
    def iswinner(self):
        cp = self.current_player
        if self.grid[0][0] == self.grid[0][1] and self.grid[0][0] == self.grid[0][2] and self.grid[0][0] != 0:
            self._winner = cp
        elif self.grid[0][0] == self.grid[1][1] and self.grid[0][0] == self.grid[2][2] and self.grid[0][0] != 0:
            self._winner = cp
        elif self.grid[2][0] == self.grid[1][1] and self.grid[1][1] == self.grid[0][2] and self.grid[1][1] != 0:
            self._winner = cp
        elif self.grid[1][0] == self.grid[1][1] and self.grid[1][0] == self.grid[1][2] and self.grid[1][0] != 0:
            self._winner = cp
        elif self.grid[0][0] == self.grid[1][0] and self.grid[0][0] == self.grid[2][0] and self.grid[0][0] != 0:
            self._winner = cp
        elif self.grid[2][0] == self.grid[2][1] and self.grid[2][0] == self.grid[2][2] and self.grid[2][0] != 0:
            self._winner = cp
        elif self.grid[0][2] == self.grid[1][2] and self.grid[0][2] == self.grid[2][2] and self.grid[0][2] != 0:
            self._winner = cp
        elif self.grid[0][1] == self.grid[1][1] and self.grid[0][1] == self.grid[2][1] and self.grid[0][1] != 0:
            self._winner = cp
    def is_over(self):
        self.update_moves()
        if len(self._possible_moves) == 0:
            return True
        else:
            return False
        
    def update_score(self):
        """
        Update score by counting umber of pairs for a given player.
        """
        last_score = self._score[len(self._score) - 1]
        score = 0
        next_player = (1 + self.current_player) % 2
        rows = {
            0 : self.grid[0],
            1 : self.grid[1],
            2 : self.grid[2]
        }
        cols = {
            0 : [self.grid[i][0] for i in range(3)],
            1 : [self.grid[i][1] for i in range(3)],
            2 : [self.grid[i][2] for i in range(3)]
        }
        diags = {
            0 : [self.grid[i][i] for i in range(3)],
            1 : [self.grid[2 - i][i] for i in range(3)]
        }
        for (id, row) in rows.items():
            if self._grid.three_in_row(row, self._marks[self._current_player]):
                score += 100
            if self._grid.three_in_row(row, self._marks[next_player]):
                score -= 100
            if self._grid.two_in_row(row, self._marks[self._current_player]):
                score += 10
            if self._grid.two_in_row(row, self._marks[next_player]):
                score -= 10
            if self._grid.one_in_row(row, self._marks[self._current_player]):
                score += 1
            if self._grid.one_in_row(row, self._marks[next_player]):
                score -= 1
        for (id, col) in cols.items():
            if self._grid.three_in_row(col, self._marks[self._current_player]):
                score += 100
            if self._grid.three_in_row(col, self._marks[next_player]):
                score -= 100
            if self._grid.two_in_row(col, self._marks[self._current_player]):
                score += 10
            if self._grid.two_in_row(col, self._marks[next_player]):
                score -= 10
            if self._grid.one_in_row(col, self._marks[self._current_player]):
                score += 1
            if self._grid.one_in_row(col, self._marks[next_player]):
                score -= 1
        for (id, diag) in diags.items():
            if self._grid.three_in_row(diag, self._marks[self._current_player]):
                score += 100
            if self._grid.three_in_row(diag, self._marks[next_player]):
                score -= 100
            if self._grid.two_in_row(diag, self._marks[self._current_player]):
                score += 10
            if self._grid.two_in_row(diag, self._marks[next_player]):
                score -= 10
            if self._grid.one_in_row(diag, self._marks[self._current_player]):
                score += 1
            if self._grid.one_in_row(diag, self._marks[next_player]):
                score -= 1
        if self.current_player == 0:
            self._score.append((score, last_score[1]))
        elif self.current_player == 1:
            self._score.append((last_score[0], score))
    def ask_move(self):
        """
        Ask player what move he wants to do.
        """
        prompt = "Player : " + str(self.current_player) + " What is your next move ? "
        answer = input(prompt)
        if CASES[answer] in OK:
            return CASES[answer]
        else : 
            self.ask_move()
    def evaluation(self, depth):
        if depth == 0 or self.winner != 2 or self.is_over() == True:
            leng = len(self._score)
            return self._score[leng - 1][1] - self._score[leng - 1][0]
        else:
            leng = len(self._score)
            if self._score[leng - 1][1] - self._score[leng - 1][0] > 0:
                return 100000 + depth
            else:
                return -100000 - depth
    
    def undo_last_move(self):
        """
        Update winner, score, current_player, last_move.
        """
        self._grid.set_case(*self.last_move[len(self._last_move) - 1], 0)

        if self.winner != 2:
            self._winner = 2

        del self._score[len(self._score) - 1]
        self._current_player -= 1
        self._current_player = self._current_player % 2
        del self._last_move[len(self._last_move) - 1]
        
        
        
    def update_moves(self):
        """
        Returns a list of possible moves in the form of (i,j).
        """
        moves = []
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    moves.append((i,j))
        self._possible_moves = moves
    def min_max(self, depth, is_max):
        """
        Met en place l'algorithme du min_max pour permettre au joueur de jouer
        contre l'ordinateur.
        """
        if self.winner != 2 or depth <= 0 or self.is_over() == True:
            return self.evaluation(depth), "N"
        else:
            if is_max:
                val = -100000
                for movement in self._possible_moves:
                    self.play(*movement, " don't show")
                    val_best_move = self.min_max(depth - 1, not is_max)
                    ia_val = val_best_move[0]
                    if val <= ia_val:
                        val = ia_val
                        best_move = movement
                    self.undo_last_move()
                    self.update_moves()
            else:
                val = 100000
                for movement in self._possible_moves:
                    self.play(*movement, "don't show")
                    val_best_move = self.min_max(depth - 1, not is_max)
                    ia_val = val_best_move[0]
                    if val >= ia_val:
                        val = ia_val
                        best_move = movement
                    self.undo_last_move()
                    self.update_moves()
            return val, best_move
    def game(self):
        self.display()
        while self.winner == 2 and self.is_over() == False:
            #print(self._possible_moves)
            if self.current_player == 0:
                move = self.ask_move()
                self.play(*move, 'show')
            else: 
                val, move = self.min_max(3, True)
                self.play(*move, 'show')

        
        
    
            
    
            