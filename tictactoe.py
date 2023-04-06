#
import os
import random


def checkWin(board):
    # check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return True
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return True
    # check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return True
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return True
    return False


def init():
    board = [[" " for i in range(3)] for j in range(3)]
    end = False
    player = 0
    aimode = ["random", "minimax", "alphabeta", "mcts", "deepReinforcementLearning"]
    asel = "minimax"
    # while asel not in aimode:
    #     os.system('cls')
    #     print("Select AI mode: ")
    #     # Join the modes with commas
    #     print("Possible modes: " + ", ".join(aimode))
    #     asel = (input("Mode: "))
    return board, end, player, asel


def minimaxHeuristic(board, moves):
    # things to consider:
    # 1. if the move is a winning move +1000
    # 2. if the move is a losing move -1000
    # 3. if the move is a draw +20
    # 4. if the move is a fork +200
    # 5. if the move allows the opponent to fork -200
    # 6. if the move creates a two in a row +200
    pass


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
        movesahead = 3
        # explore all possible moves
        all_moves = minimax_explore_moves(cboard, movesahead)
        # then analize heuristics of each move
        row, col = minimaxHeuristic(all_moves)

    elif asel == "alphabeta":
        pass
    elif asel == "mcts":
        pass
    elif asel == "deepReinforcementLearning":
        pass
    return row, col


def game(board, player, asel):
    os.system("cls" if os.name == "nt" else "clear")
    print("Actual board:")
    for row in board:
        print(row)
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
        end = checkWin(board)

    print("Actual board:")
    for row in board:
        print(row)
    print("Player 1 wins!" if (player + 1) % 2 == 0 else "AI wins!")


main()