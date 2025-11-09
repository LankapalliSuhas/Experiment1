import json
import random

class Sudoku:
    def __init__(self):
        # Data Structures: 2D list for grid, lists of sets for row/col/box tracking
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.row = [set() for _ in range(9)]
        self.col = [set() for _ in range(9)]
        self.box = [set() for _ in range(9)]

    def _update_sets(self):
        # Basic Programming: Loops and conditionals to populate sets
        for i in range(9):
            self.row[i].clear()
            self.col[i].clear()
            self.box[i].clear()
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    num = self.grid[i][j]
                    self.row[i].add(num)
                    self.col[j].add(num)
                    box_index = (i // 3) * 3 + (j // 3)
                    self.box[box_index].add(num)

    def load_from_file(self, filename):
        # File Handling: Read JSON file
        with open(filename, 'r') as file:
            data = json.load(file)
            self.grid = data['grid']
        self._update_sets()

    def save_to_file(self, filename):
        # File Handling: Write JSON file
        with open(filename, 'w') as file:
            json.dump({'grid': self.grid}, file)

    def find_empty(self):
        # Function: Basic loop to find empty cell (data structure traversal)
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, row, col, num):
        # Function: Check validity using sets (data structures)
        box_index = (row // 3) * 3 + (col // 3)
        if num not in self.row[row] and num not in self.col[col] and num not in self.box[box_index]:
            return True
        return False

    def solve(self):
        # OOP Method: Backtracking function (basic concepts: recursion, loops, if-else)
        empty = self.find_empty()
        if not empty:
            return True  # Solved
        i, j = empty
        for num in range(1, 10):
            if self.is_valid(i, j, num):
                self.grid[i][j] = num
                self.row[i].add(num)
                self.col[j].add(num)
                box_index = (i // 3) * 3 + (j // 3)
                self.box[box_index].add(num)
                if self.solve():
                    return True
                # Backtrack
                self.grid[i][j] = 0
                self.row[i].remove(num)
                self.col[j].remove(num)
                self.box[box_index].remove(num)
        return False

    def generate_puzzle(self, cells_to_remove=40):
        # OOP Method: Generate puzzle using backtracking (small AI tool: randomized search algorithm)
        # Step 1: Fill diagonal boxes (basic loop, random shuffle)
        for box in range(0, 9, 3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            index = 0
            for i in range(3):
                for j in range(3):
                    r = (box // 3) * 3 + i
                    c = (box % 3) * 3 + j
                    self.grid[r][c] = nums[index]
                    self.row[r].add(nums[index])
                    self.col[c].add(nums[index])
                    self.box[box].add(nums[index])
                    index += 1
        # Step 2: Solve to fill the rest (uses solve method)
        self.solve()
        # Step 3: Remove cells for puzzle (loop, random shuffle)
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        for k in range(cells_to_remove):
            i, j = cells[k]
            num = self.grid[i][j]
            self.grid[i][j] = 0
            self.row[i].remove(num)
            self.col[j].remove(num)
            box_index = (i // 3) * 3 + (j // 3)
            self.box[box_index].remove(num)
        self._update_sets()  # Update after removals
