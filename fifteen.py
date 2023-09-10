# fifteen.py is a program that implements a Fifteen class to set up and allow users to play the Fifteen puzzle

import numpy as np
from random import choice
import math

class Fifteen:
    
    # create a vector (ndarray) of tiles and the layout of tiles positions (a graph)
    # tiles are numbered 1-15, the last tile is 0 (an empty space)
    def __init__(self, size = 4):
        self.tiles = np.array([i for i in range(1,size**2)] + [0]) # array of tiles
        self.solution = np.array([i for i in range(1,size**2)] + [0]) # array of end solution of puzzle, set to tiles 1-15 in order with empty space in bottom right corner
        self.vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] # list of vertices (tile positions on board)
        self.adj = [[1,4], [0,2,5], [1,3,6], [2,7], [0,5,8], [1,4,6,9], [2,5,7,10], [3,6,11], [4,9,12], [5,8,10,13], [6,9,11,14], [7,10,15], [8,13], [9,12,14], [10,13,15], [11,14]] # adjacency list to track neighbors of vertices   

    # update the vector of tiles
    # if the move is valid assign the vector to the return of transpose() or call transpose     
    def update(self, move):
        if self.is_valid_move(move): # check if move is valid
            self.transpose(0, move) # transpose empty tile and the move
    
    # exchange i-tile with j-tile  
    # tiles are numbered 1-15, the last tile is 0 (empty space) 
    # the exchange can be done using a dot product (not required)
    # can return the dot product (not required)        
    def transpose(self, i, j):
        i_index=np.where(self.tiles == i) # find index of i-tile in tiles array
        j_index=np.where(self.tiles == j) # find index of j-tile in tiles array
        self.tiles[i_index], self.tiles[j_index] = self.tiles[j_index], self.tiles[i_index] # swap the tiles
    
    # shuffle tiles
    def shuffle(self, steps=100):
        index = np.where(self.tiles == 0)[0][0] # find the empty space
        for x in range(steps): # swap tiles 100 times
            move_index = choice (self.adj[index]) # randomly select a neighbor of index
            self.tiles[index],self.tiles[move_index] = self.tiles[move_index],self.tiles[index] # swap the tiles
            index = move_index # set index to the new empty space
        
    # checks if the move is valid: one of the tiles is 0 and another tile is its neighbor         
    def is_valid_move(self, move):
        vertex = np.where(self.tiles == move)[0][0] # find the vertex the tile is at
        adj_verts = self.adj[vertex] 
        for x in adj_verts: # traverse the list of neighboring vertices
            if self.tiles[x]==0: # if the 0 tile is one of the neighbors, return True
                return True
        return False # if the tile is not adjacent to the 0 tile, return False

    # verify if the puzzle is solved    
    def is_solved(self):
        for x in range(self.tiles.size): # traverse through tiles and check if each tile is equal to corresponding tile in solution array
            if self.tiles[x] != self.solution[x]: # if one of the tiles don't match, return False
                return False
        return True # if all the tiles match, return True
    
    # draw the layout with tiles:
    # +---+---+---+---+
    # | 1 | 2 | 3 | 4 |
    # +---+---+---+---+
    # | 5 | 6 | 7 | 8 |
    # +---+---+---+---+
    # | 9 |10 |11 |12 |
    # +---+---+---+---+
    # |13 |14 |15 |   |
    # +---+---+---+---+
    def draw(self):
        size = math.sqrt(self.tiles.size) # number of rows/columns
        count = 0
        for x in range(int(size)): # creates 4 rows
            print("+---+---+---+---+")
            for y in range(int(size)): # creates 4 columns
                print("|", end='')
                if self.tiles[count]<10:
                    print(" ", end='')
                if self.tiles[count]==0: # empty tile
                    print("  ", end='')
                else:
                    print(str(self.tiles[count]) + " ", end='') # print tile number
                count+=1
            print("|")
        print("+---+---+---+---+")
            
    # return a string representation of the vector of tiles as a 2d array  
    # 1  2  3  4
    # 5  6  7  8
    # 9 10 11 12
    #13 14 15         
    def __str__(self):
        str_ = " "
        orig_str = str(self.tiles) # ex: for original board: orig_str would be "[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15  0]"
        num_count = 0
        for x in range(len(orig_str)): # traverse through string
            if orig_str[x].isdigit(): # if the character is a digit
                number = ""
                y = x
                while y!=len(orig_str) and orig_str[y].isdigit(): # keep traversing through string and check if number has more digits
                    number += orig_str[y]
                    y += 1
                if number != "":
                    num_count += 1 # add to count of numbers
                    if number == "0": # if number is zero, add empty spaces
                        str_ += "   "
                    else: # otherwise add the number and a space to the string
                        str_ += number + " "
                    if num_count % 4 == 0: # if row has 4 numbers already, add new line to create new row
                        str_ += "\n"
                    if num_count<9: # two spaces between one-digit numbers
                        str_ += " "
                    while y!=x: # go back and replace digits in number to * to avoid repetition of numbers during traversal
                        orig_str = orig_str[:(y-1)] + "*" + orig_str[(y-1) + 1:]
                        y-=1
                    number = ""
        return str_ # return the string
    
if __name__ == '__main__':
    # test code
    game = Fifteen()
    assert str(game) == ' 1  2  3  4 \n 5  6  7  8 \n 9 10 11 12 \n13 14 15    \n'
    assert game.is_valid_move(15) == True
    assert game.is_valid_move(12) == True
    assert game.is_valid_move(14) == False
    assert game.is_valid_move(1) == False
    game.update(15)
    assert str(game) == ' 1  2  3  4 \n 5  6  7  8 \n 9 10 11 12 \n13 14    15 \n'
    game.update(15)
    assert str(game) == ' 1  2  3  4 \n 5  6  7  8 \n 9 10 11 12 \n13 14 15    \n'
    assert game.is_solved() == True
    game.shuffle()
    assert str(game) != ' 1  2  3  4 \n 5  6  7  8 \n 9 10 11 12 \n13 14 15    \n'
    assert game.is_solved() == False

    # main program
    game = Fifteen()
    game.shuffle()
    game.draw()
    while True:
        move = input('Enter your move or q to quit: ')
        if move == 'q':
            break
        elif not move.isdigit():
            continue
        game.update(int(move))
        game.draw()
        if game.is_solved():
            break
    print('Game over!')
