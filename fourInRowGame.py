import numpy as np
from enum import Enum
import warnings
import math


class Chip(Enum):
    EMPTY = 0
    YELLOW = 1
    RED = 2

    def short(self):
        if self == self.EMPTY:
            return "-"
        if self == self.RED:
            return "R"
        if self == self.YELLOW:
            return "Y"

class FourInRowGame:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.slots = np.full((self.rows, self.columns), fill_value=Chip.EMPTY, dtype=Chip)
        self.last_chip = None

    def reset(self):
        self.slots = np.full((self.rows, self.columns), fill_value=Chip.EMPTY, dtype=Chip)
        self.last_chip = None

    def play_game(self, chip, column):
        if self.last_chip == chip:
            warnings.warn("One player played multiple times in a row", Warning)
        self.last_chip = chip

        self.drop(chip, column)
        victory_detected = self.check_for_victory()
        return victory_detected
    
    def valid_drop(self, chip, column):
        # check column exists
        if column >= self.columns:
            return False
        # check column not full
        elif self.column_height(column) >= self.rows:
            return False
        else:
            return True
        
    #check if all columns are full
    def field_is_full(self):
        for col in range(self.columns):
            if self.column_height(col) == self.rows:
                pass
            else:
                return False
        return True   
    
    def column_is_full(self,column):
        if self.column_height(column) == self.rows:
            pass
        else:
            return False
        return True   
    

    #useful for iterating/simulating different actions
    def get_next_moves(self):
        possibilities = []
        for col in range(self.columns):
            if self.column_height(col) == self.rows:
                pass
            else:
                possibilities.append(col)
        return possibilities  

    def drop(self, chip, column):
        # check column exists
        if column >= self.columns:
            raise ValueError(f"Column {column} does not exist")
        # check column not full
        if self.column_height(column) >= self.rows:
            raise ValueError(f"Column {column} is already filled")
        
        selected_row = self.rows
        while selected_row != 0 and self.slots[selected_row - 1, column] == Chip.EMPTY:
            selected_row = selected_row - 1
        
        self.slots[selected_row, column] = chip


    def column_height(self, column):
        selected_row = self.rows
        while selected_row != 0 and self.slots[selected_row - 1, column] == Chip.EMPTY:
            selected_row = selected_row - 1
        return selected_row
    
    def check_for_victory(self):
        for row in range(self.rows):
            for column in range(self.columns):
                base_chip = self.slots[row, column]
                if base_chip == Chip.EMPTY:
                    continue
                #horizontal victory
                if column <= self.columns - 4:
                    if(self.slots[row, column + 1] == base_chip and 
                        self.slots[row, column + 2] == base_chip and
                        self.slots[row, column + 3] == base_chip):
                        return True
                #vertical victory
                if row <= self.rows - 4:
                    if(self.slots[row + 1, column] == base_chip and 
                        self.slots[row + 2, column] == base_chip and
                        self.slots[row + 3, column] == base_chip):
                        return True
                #diagonal right victory
                if column <= self.columns - 4 and row <= self.rows - 4:
                    if(self.slots[row + 1, column + 1] == base_chip and 
                        self.slots[row + 2, column + 2] == base_chip and
                        self.slots[row + 3, column + 3] == base_chip):
                        return True
                #diagonal left victory
                if column - 3 >= 0 and row <= self.rows - 4:
                    if(self.slots[row + 1, column - 1] == base_chip and 
                        self.slots[row + 2, column - 2] == base_chip and
                        self.slots[row + 3, column - 3] == base_chip):
                        return True
        return False
    
    #check which color has won
    def check_for_victory_red(self):
        for row in range(self.rows):
            for column in range(self.columns):
                base_chip = self.slots[row, column]
                if base_chip == Chip.EMPTY:
                    continue
                #horizontal victory
                if column <= self.columns - 4:
                    if(self.slots[row, column + 1] == base_chip and 
                        self.slots[row, column + 2] == base_chip and
                        self.slots[row, column + 3] == base_chip):
                        return True if Chip.RED == base_chip else False 
                #vertical victory
                if row <= self.rows - 4:
                    if(self.slots[row + 1, column] == base_chip and 
                        self.slots[row + 2, column] == base_chip and
                        self.slots[row + 3, column] == base_chip):
                        return True if Chip.RED == base_chip else False
                #diagonal right victory
                if column <= self.columns - 4 and row <= self.rows - 4:
                    if(self.slots[row + 1, column + 1] == base_chip and 
                        self.slots[row + 2, column + 2] == base_chip and
                        self.slots[row + 3, column + 3] == base_chip):
                        return True if Chip.RED == base_chip else False
                #diagonal left victory
                if column - 3 >= 0 and row <= self.rows - 4:
                    if(self.slots[row + 1, column - 1] == base_chip and 
                        self.slots[row + 2, column - 2] == base_chip and
                        self.slots[row + 3, column - 3] == base_chip):
                        return True if Chip.RED == base_chip else False
        return False

    #extract all windows of 4 connected fields to evaluate position 
    def evaluate_positions(self):
        total_util = 0
        positions = []
        #horizontal window
        for row in range(self.rows):
            for col in range(self.columns- 3):
                window = self.slots[row, col:col + 4]
                util = self.evaluate_window(window,'s')
                if util !=0:
                    positions.append(['h',util,row,col])
                total_util += util
            
        # vertical window
        for row in range(self.rows - 3):
            for col in range(self.columns):
                window = self.slots[row:row + 4, col]
                util = self.evaluate_window(window,'s')
                if util !=0:
                    positions.append(['v',util,row,col])
                total_util += util
    
        # Check positively sloped diagonal scores
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                window = [self.slots[row + i, col + i] for i in range(4)]
                util = 0#self.evaluate_window(window,'d')
                if util !=0:
                    positions.append(['r',util,row,col])
                total_util += util
    
        # Check negatively sloped diagonal scores
        for row in range(self.rows - 3):
            for col in range(3,self.columns):
                window = [self.slots[row + 3 - i, col - 3 + i] for i in range(4)]
                util = 0#self.evaluate_window(window,'d')
                if util !=0:
                    positions.append(['l',util,row,col])
                total_util += util
                
        return total_util#,positions
                                        
    #Add a flag if window is straight(hoizontal/vertical) or diagonal
    #diagonal windows have lower values because they require more chips to build 
    def evaluate_window(self, window,flag):
        # if chips of different color are in a window, the window cannot be won
        # therefore no utility for both players
        if Chip.RED in window and Chip.YELLOW in window:
            return 0
        
        #if no chip in window the window has not been used so far
        #therefore no utility for both players
        if Chip.RED not in window and Chip.YELLOW not in window:
            return 0
        
        #if only one color in window estimate utility
        #the more free slots are in the window the less utility it has
        #e.g. if 3 out of the 4 fields are filled with red 
        #position is better than just one out of 4 filled with red
        if Chip.RED in window and Chip.YELLOW not in window:
            no_of_chips = [chip == Chip.RED for chip in window]
            if sum(no_of_chips) == 1:
                return 0
            elif sum(no_of_chips) == 2:
                return 20
            elif sum(no_of_chips) == 3:
                return 10000
            else:
                #only option left is 4 of a kind and thats a win
                return math.inf
            
        if Chip.YELLOW in window and Chip.RED not in window:
            no_of_chips = [chip == Chip.YELLOW for chip in window]
            if sum(no_of_chips) == 1:
                return -0
            elif sum(no_of_chips) == 2:
                return -20
            elif sum(no_of_chips) == 3:
                return -10000
            else:
                #only option left is 4 of a kind and thats a win
                return -math.inf                        
    
    #create a copy of a existing environment
    #useful for iterating/simulating different actions
    def get_env_copy(self):
        env_copy = FourInRowGame(self.rows, self.columns)
        env_copy.slots = np.copy(self.slots)
        return env_copy

    def get_simple_slots(self):
        slots = np.zeros((self.rows, self.columns), dtype=int)
        for row in range(self.rows):
            for column in range(self.columns):
                slots[row, column] = self.slots[row, column].value
        return slots
    
    def get_simple_slots_negative(self):
        slots = np.zeros((self.rows, self.columns), dtype=int)
        for row in range(self.rows):
            for column in range(self.columns):
                slots[row, column] = -1 if self.slots[row, column].value == 2 else self.slots[row, column].value
        return slots

    def print(self):
        for i in range(self.rows - 1, -1, -1):
            print("")
            for j in range(self.columns):
                print(f"{self.slots[i,j].short()} ", end="")