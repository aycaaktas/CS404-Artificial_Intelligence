import copy
from enum import Enum
from queue import PriorityQueue
import math





Move = Enum('Move', ["up", "down", "right", "left"])

class Node:
    def __init__(self, state, f, parent=None, direction=None):
        self.state = state
        self.f = f
        self.parent = parent
        self.direction = direction # param direction shows which direction is to be selected to reach from the parent node to this node


    def __lt__(self, other):
     
      return self.f < other.f


class GameBoard:

  def __init__(self, grid):
        self.grid = [list(row) for row in grid]  # Make a copy of the grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.g = 0
        # Identify the starting position of the agent ('S')
        for i in range(self.rows):
            for j in range(self.cols):
                if grid[i][j] == 'S':
                    self.agent_pos = [i, j]
                    break

  def transpose_grid(self):

    temp = self.agent_pos[1]
    self.agent_pos[1] = self.agent_pos[0]
    self.agent_pos[0] = temp
    self.grid =[list(row) for row in zip(*self.grid)]



  def color_cell_predict(self, movement: Move):
       
        distance = 0
        row_index = self.agent_pos[0]
        col_index = self.agent_pos[1]

        if movement == Move.right:
            for col_no, cell in enumerate(self.grid[row_index][col_index:], start=col_index):
                if cell == "X":
                  break
                if cell == "0":
                  distance += 1

        elif movement == Move.left:

          relevant_row_part = []
          for i in range(col_index + 1):
            element = self.grid[row_index][i]
            relevant_row_part.append((i, element))
          for col_no, cell in reversed(relevant_row_part):
                if cell == "X":
                    break
                if cell == "0":
                    distance += 1

        elif movement == Move.down:
            self.transpose_grid()
            counter = self.color_cell_predict(Move.right)
            self.transpose_grid()

        elif movement == Move.up:
            self.transpose_grid()
            counter = self.color_cell_predict(Move.left)
            self.transpose_grid()

        if distance == 1:
            return float('inf')
        else:
            return distance

  def move_cell(self, movement) :

        row_index = self.agent_pos[0]
        col_index = self.agent_pos[1]

        if movement == Move.right:
            for col_no, cell in enumerate(self.grid[row_index][col_index:], start=col_index):
                if cell == "X":
                    self.grid[row_index][col_no - 1] = "S"
                    self.agent_pos[1] = col_no - 1
                    break

                self.grid[row_index][col_no] = "1"
                self.g += 1

                if col_no == len(self.grid[row_index]) - 1:  # if the cell is at the edge of the board
                    self.grid[row_index][col_no] = "S"
                    self.agent_pos[1] = col_no

        elif movement == Move.left:

            current_row = list(enumerate(self.grid[row_index]))
            current_row = current_row[:col_index + 1]
            for col_no, cell in reversed(current_row):
                if cell == "X":
                    self.grid[row_index][col_no + 1] = "S"
                    self.agent_pos[1] = col_no + 1
                    break

                self.grid[row_index][col_no] = "1"
                self.g += 1

                if col_no == 0:  # if the cell is at the edge of the board
                    self.grid[row_index][col_no] = "S"
                    self.agent_pos[1] = col_no

        elif movement == Move.down:
            self.transpose_grid()
            self.move_cell(Move.right)
            self.transpose_grid()

        elif movement == Move.up:
            self.transpose_grid()
            self.move_cell(Move.left)
            self.transpose_grid()

  def move_cost(self, movement):

        distance = 1
        row_index = self.agent_pos[0]
        col_index = self.agent_pos[1]

        if movement == Move.right:
            for cell in self.grid[row_index][col_index:]:
                if cell == "X":
                    break
                elif cell == "0" or cell == "1":
                    distance += 1
        
        elif movement == Move.left:
            current_row =  reversed(self.grid[row_index][:col_index + 1])
            for cell in current_row:
                if cell == "X":
                    break
                elif cell == "0" or cell == "1":
                    distance += 1

        elif movement == Move.down:
            self.transpose_grid()
            counter = self.move_cost(Move.right)
            self.transpose_grid()
        
        elif movement == Move.up:
            self.transpose_grid()
            counter = self.move_cost(Move.left)
            self.transpose_grid()

        return distance

  def heuristic_calc(self, movement) :

        if movement == Move.down or movement == Move.up:
            return len(self.grid) - self.color_cell_predict(movement)
        elif movement == Move.left or movement == Move.right:
            return len(self.grid[0]) - self.color_cell_predict(movement)
        
  def heuristic_calc2(self, movement) :    
    
    empty_cells = sum(row.count(0) for row in self.grid)
    rows = len(self.grid)
    cols = len(self.grid[0]) if rows > 0 else 0
    diagonal_distance = math.sqrt(rows**2 + cols**2)
    return empty_cells * diagonal_distance
       
        

  def goal_test(self):

        for row in self.grid:
            for cell in row:
                if cell == "0":
                    return False
        return True

