import numpy as np
from enum import Enum
import warnings


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

    def get_simple_slots(self):
        slots = np.zeros((self.rows, self.columns), dtype=int)
        for row in range(self.rows):
            for column in range(self.columns):
                slots[row, column] = self.slots[row, column].value
        return slots

    def print(self):
        for i in range(self.rows - 1, -1, -1):
            print("")
            for j in range(self.columns):
                print(f"{self.slots[i,j].short()} ", end="")