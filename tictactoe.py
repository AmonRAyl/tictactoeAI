#
import os
import random


def checkWin(board, player):
    winning_combinations = [
        # rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]
    for combination in winning_combinations:
        if all(board[row][col] == "X" for row, col in combination) and (player == 2 or player == 0):
            return True
        elif all(board[row][col] == "0" for row, col in combination) and player == 1:
            return True
    return False


def init():
    board = [[" " for i in range(3)] for j in range(3)]
    end = False
    player = 0
    aimode = ["random", "minimax", "alphabeta", "mcts", "deepReinforcementLearning"]
    asel = "minimax"
    # while asel not in aimode:
    # os.system("cls" if os.name == "nt" else "clear")
    #     print("Select AI mode: ")
    #     # Join the modes with commas
    #     print("Possible modes: " + ", ".join(aimode))
    #     asel = (input("Mode: "))
    return board, end, player, asel

def printBoard(board):
    os.system("cls" if os.name == "nt" else "clear")
    print("Actual board:")
    for row in board:
        print(row)

def checkTwoInRow(board, player):
    total = 0
    
    # Check rows
    for row in board:
        if row.count("X" if player == 0 else "O") == 2 and row.count(" ") == 1:
            total+=1
    
    # Check columns
    for j in range(3):
        col = [board[i][j] for i in range(3)]
        if col.count("X" if player == 0 else "O") == 2 and col.count(" ") == 1:
            total+=1
    
    # Check diagonals
    diag1 = [board[i][i] for i in range(3)]
    if diag1.count("X" if player == 0 else "O") == 2 and diag1.count(" ") == 1:
        total+=1
    
    diag2 = [board[i][2-i] for i in range(3)]
    if diag2.count("X" if player == 0 else "O") == 2 and diag2.count(" ") == 1:
        total+=1
    
    return total
def getminormax(moves, minormax):
    if minormax=="min":
        minscore=100000000
        for j in moves:#in doesnt work for the first case
            b=j.copy()
            while len(b[1])!=3: #i should maybe use isinstance or smth to check if it is list as if the game advanceses number of moves might be 3
                b=b[1]
            if b[1][2]<minscore:
                minscore=b[1][2]
                bestmove=j
    else:
        maxscore=-100000000
        for j in moves:
            b=j.copy()
            while len(b[1])!=3:
                b=b[1]
            if b[1][2]>maxscore:
                maxscore=b[1][2]
                bestmove=j
    return bestmove

    
def minimaxHeuristic(cboard, moves,movesahead):
    score=0
    count=0
    #apply first set of moves from the list , it is currently hardocded to 4 moves ahead
    for set in moves:
        row,col=set[0]
        cboard[row][col]="0" if count%2==0 else "X"
        count+=1
        for s_moveahead in (set[1]):
            row1,col1=s_moveahead[0]
            cboard[row1][col1]="0" if count%2==0 else "X"
            count+=1
            for t_moveahead in (s_moveahead[1]):
                row2,col2=t_moveahead[0]
                cboard[row2][col2]="0" if count%2==0 else "X"
                count+=1
                for f_moveahead in (t_moveahead[1]):
                    row3,col3=f_moveahead
                    cboard[row3][col3]="0" if count%2==0 else "X"
                    count+=1
                    score=0
                    minscore=500000
                    #check if position can exist 
                    if checkWin(cboard,1)==True and checkWin(cboard,0)==True:
                        score=0
                    else:
                        # 1. if you won +1000 if you lost -1000
                        if checkWin(cboard,0):
                            score-=2000
                        if checkWin(cboard,1):
                            score+=2000
                        #check if oponent has a two in a row
                        if checkTwoInRow(cboard,1)!=0:
                            score+=800
                        if checkTwoInRow(cboard,0)!=0:
                            score-=300*checkTwoInRow(cboard,0)
                    f_moveahead.append(score)
                    if minscore>score:
                        minscore=score
                        bestmove=f_moveahead
                    cboard[row3][col3]=" "
                    count-=1
                t_moveahead[1]=bestmove
                #t_moveahead[1]=getminormax(t_moveahead[1],"min") #select min
                cboard[row2][col2]=" "
                count-=1
            s_moveahead[1]=getminormax(s_moveahead[1],"max") #select max
            cboard[row1][col1]=" "
            count-=1
        set[1]=getminormax(set[1],"min") #select min
        cboard[row][col]=" "
        count-=1
    moves=getminormax(moves,"max") #select max
    return moves[0]


def minimax_explore_moves(cboard, movesahead):
    if movesahead == 0:
        return []

    possiblemoves = []
    for row in range(3):
        for col in range(3):
            if cboard[row][col] == " ":
                possiblemoves.append([row, col])

    explored_moves = []

    for j in possiblemoves:
        row, col = j

        # If the move is valid, make it and recursively explore the resulting board
        if cboard[row][col] == " ":
            if movesahead % 2 == 0:
                cboard[row][col] = "O"
            else:
                cboard[row][col] = "X"  # Assuming it's X's turn

            # Recursively explore the resulting board and append the explored moves to the current list
            returned_moves = minimax_explore_moves(cboard, movesahead - 1)
            if returned_moves != []:
                explored_moves.append([j, returned_moves])
            else:
                explored_moves.append(j)

            cboard[row][col] = " "  # Undo the move

    # Return the list of explored moves till movesahead depth
    return explored_moves


def aiselector(board, asel):
    # copy board to not modify the original
    cboard = [row[:] for row in board]
    if asel == "random":
        while True:
            row, col = random.randint(0, 2), random.randint(0, 2)
            if cboard[row][col] == " ":
                break
    elif asel == "minimax":
        movesahead = 4
        # explore all possible moves
        all_moves = minimax_explore_moves(cboard, movesahead)#when it checks 4 moves ahead it has to look if there can be done , as when the game advanceses less moves are going to be possible until there are less than 4
        # then analize heuristics of each move
        row, col = minimaxHeuristic(cboard,all_moves,movesahead)

    elif asel == "alphabeta":
        pass
    elif asel == "mcts":
        pass
    elif asel == "deepReinforcementLearning":
        pass
    return row, col


def game(board, player, asel):
    printBoard(board)
    if player == 0:
        print("Player 1's turn")
        print("Enter the row and column of the square you want to place your X in")
        row = int(input("Row: "))
        col = int(input("Column: "))
        board[row][col] = "X"
    else:
        row, col = aiselector(board, asel)  # AI's turn
        board[row][col] = "O"
    return (player + 1) % 2


def main():
    board, end, player, asel = init()

    while not end:
        player = game(board, player, asel)
        end = checkWin(board,2)

    printBoard(board)
    print("Player 1 wins!" if (player + 1) % 2 == 0 else "AI wins!")


main()