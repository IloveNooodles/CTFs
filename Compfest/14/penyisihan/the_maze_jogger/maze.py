#!/usr/bin/env python3
import random
import math
import signal
import time

WIDTH = random.randint(15, 20)
HEIGHT = WIDTH

class Timeout(Exception):
    pass

class Maze():
    def __init__(self, width, height):
        self.maze = []
        for i in range(height):
            cols = []
            for j in range(width):
                cols.append(None)
            self.maze.append(cols)
        
    def __repr__(self):
        return f"{self.maze}"

class Cell():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = [1, 1, 1, 1] # N E S W
        self.visited = False
        
    def __repr__(self):
        return f"({self.row}, {self.col}) Walls: {self.walls}"

class Player():
    def __init__(self, maze, cell):
        self.maze = maze
        self.cell = cell
        
    def move_forward(self):
        if self.cell.walls[1] == 0:
            self.cell = self.maze.maze[self.cell.row][self.cell.col + 1]
            return True
        return False
        
    def move_backward(self):
        if self.cell.walls[3] == 0:
            self.cell = self.maze.maze[self.cell.row][self.cell.col - 1]
            return True
        return False
        
    def move_right(self):
        if self.cell.walls[2] == 0:
            self.cell = self.maze.maze[self.cell.row + 1][self.cell.col]
            return True
        return False
        
    def move_left(self):
        if self.cell.walls[0] == 0:
            self.cell = self.maze.maze[self.cell.row - 1][self.cell.col]
            return True
        return False

def handler(sig, frame):
    raise Timeout

def init_maze(maze):
    for i in range(WIDTH):
        for j in range(HEIGHT):
            maze.maze[i][j] = Cell(i, j)

    curr = maze.maze[0][0]
    curr.visited = True
    stack = [curr]
    
    while stack:
        curr = stack.pop()
        neighbors = []
        if curr.row < HEIGHT - 1:
            neighbors.append(maze.maze[curr.row + 1][curr.col])
        if curr.row > 0:
            neighbors.append(maze.maze[curr.row - 1][curr.col])
        if curr.col < WIDTH - 1:
            neighbors.append(maze.maze[curr.row][curr.col + 1])
        if curr.col > 0:
            neighbors.append(maze.maze[curr.row][curr.col - 1])
        
        unvisited_neighbors = []
        for neighbor in neighbors:
            if not neighbor.visited:
                unvisited_neighbors.append(neighbor)
        
        if unvisited_neighbors:
            stack.append(curr)
            next_cell = unvisited_neighbors[random.randint(0, len(unvisited_neighbors) - 1)]
            if next_cell.row == curr.row + 1:
                curr.walls[2] = 0
                next_cell.walls[0] = 0
            elif next_cell.row == curr.row - 1:
                curr.walls[0] = 0
                next_cell.walls[2] = 0
            elif next_cell.col == curr.col + 1:
                curr.walls[1] = 0
                next_cell.walls[3] = 0
            elif next_cell.col == curr.col - 1:
                curr.walls[3] = 0
                next_cell.walls[1] = 0
            next_cell.visited = True
            stack.append(next_cell)

def show_intro():
    title = """
       _____                           ________                       
      /     \ _____  ________ ____    /  _____/_____    _____   ____  
     /  \ /  \\\__  \ \___   // __ \  /   \  ___\__  \  /     \_/ __ \ 
    /    Y    \/ __ \_/    /\  ___/  \    \_\  \/ __ \|  Y Y  \  ___/ 
    \____|__  (____  /_____ \\\___  >  \______  (____  /__|_|  /\___  >
            \/     \/      \/    \/          \/     \/      \/     \/ 
    """
    print(title)
    print("Welcome to the maze! You will not know where the end of the maze is, but you'll sense where you are and how far the destination is.")
    print("Take your time and don't rush, except if you want to be free! Mwahahahaha~\n")

def main():
    print("Generating maze.....")
    maze = Maze(WIDTH, HEIGHT)
    init_maze(maze)
    winning_cell = maze.maze[random.randint(0, HEIGHT - 1)][WIDTH - 1]
    
    print("Initializing player.....\n")
    player = Player(maze, maze.maze[random.randint(0, HEIGHT - 1)][0])
    
    show_intro()
    
    while True:
        if player.cell == winning_cell:
            print("Wowie zowie you've made it. :o")
            print(open("flag.txt", "r").read())
            print(f"Final Position: ({player.cell.row} {player.cell.col})")
            return
            
        dist = math.sqrt(pow(winning_cell.row - player.cell.row, 2) + pow(winning_cell.col - player.cell.col, 2)) 
        print(f"Position: ({player.cell.row} {player.cell.col})")
        print(f"Distance from prize: {dist}")
        
        inp = input("What do you wanna do?\n1) Move forward\n2) Move backward\n3) Move right\n4) Move left\n5) Surrender\n>>> ")
        
        if inp == '1':
            if player.move_forward():
                print("Moved forward.")
            else:
                print("Can't move forward.")
        elif inp == '2':
            if player.move_backward():
                print("Moved backward.")
            else:
                print("Can't move backward.")
        elif inp == '3':
            if player.move_right():
                print("Moved right.")
            else:
                print("Can't move right.")
        elif inp == '4':
            if player.move_left():
                print("Moved left.")
            else:
                print("Can't move left.")
        elif inp == '5':
            print("Thou hast been vanquished!")
            return
        else:
            print("You can't do that lmao!")
            
        print()
    
if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(30)
    try:
        exit(main())
    except Timeout:
        print("Too weak, too slow!")
