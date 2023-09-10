# game.py is a program that creates a GUI Fifteen Puzzle using tkinter

from tkinter import *
import tkinter.font as font
from fifteen import Fifteen
from random import choice

def clickButton(value, pos):
    global empty, board
    if value.get()!='': # check that the button being clicked on is not the empty space
        if board.is_valid_move(int(value.get())): # check if the move is valid
            board.update(int(value.get())) # update the board using the Fifteen method
            labels[empty].set(value.get()) # update the label of the empty button
            empty = pos-1 # update the empty global variable
            labels[pos-1].set('') # change the button being clicked on to be the empty space
    if board.is_solved(): # if the board has been solved, create "You win!" text at the bottom of the screen
        win_text = Text(gui, bg='white', fg='black',font=font2, height=2, width=20) 
        win_text.tag_configure("center", justify='center')
        win_text.insert(END, "You win!")
        win_text.tag_add("center", "1.0", "end")
        win_text.grid(row=5, column=0, columnspan=4)

def addButton(gui, value, pos): # value is a tile label and pos a tile position on the board
    # create a Button with text as value and name as pos, and bind it to clickButton function
    return Button(gui, textvariable=value, name=str(pos), bg='white', fg='black', font=font1, height=2, width=5, command = lambda: clickButton(value, pos))

def shuffle(count, number): # shuffle tiles
    global empty, board 
    if count < number: # will swap tiles the given number of times 
        move_index = choice (board.adj[empty]) # randomly select a neighbor of empty space
        board.update(int(labels[move_index].get())) # update the board using the Fifteen method
        labels[empty].set(labels[move_index].get()) # update the label of the empty button
        empty = move_index # update the empty global variable
        labels[empty].set('') # change the neighboring tile to be the empty space
        gui.after(50, lambda: shuffle(count+1,number)) # animate shuffle of tiles

if __name__ == '__main__':    
    # make a board with tiles
    board = Fifteen()
    empty = 15
    # make a window
    gui = Tk()
    gui.title("Fifteen")
    # make fonts
    font1 = font.Font(family='Helveca', size='25', weight='bold')
    font2 = font.Font(family='Times', size='50', weight='bold')
    # make buttons with labels
    labels = []
    buttons = []
    for x in range(board.tiles.size): # traverse through tiles
        labels.append(StringVar()) # add a StringVar() to labels list
        if board.tiles[x]==0: # set label of empty button to ''
            labels[x].set('')
        else: # add tiles to labels list
            labels[x].set(str(board.tiles[x]))
        button = addButton(gui, labels[x], board.vertices[x]) # create button with corresponding label and vertex
        buttons.append(button) # add button to buttons list

    # arrange buttons on the grid
    row_num = 0
    col_num = 0
    for x in buttons: # traverse through buttons list
        x.grid(row=row_num, column=col_num) # add button to grid
        col_num+=1
        if col_num == 4: # if 4 buttons already on a row, move to new row and restart at first column
            row_num += 1
            col_num = 0

    # add a button shuffle to shuffle the tiles
    label_shuffle = StringVar() # create label for button
    label_shuffle.set('shuffle')
    shuffle_button = Button(gui, textvariable=label_shuffle, name='shuffle', bg='white', fg='black', font=font1, height=2, width=10, command = lambda : shuffle(0, 100)) # bind button to shuffle function
    shuffle_button.grid(row=4, column=1, columnspan=2) # add button under tiles
            
    # update the window
    gui.mainloop()
