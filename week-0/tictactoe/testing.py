import tictactoe as ttt
import sys

# Testing and debugging file


def print_board(board: list[list[str | None]]):
    for row in board:
        for token in row:
            print(token + " " if token is not None else "· ", end="")
        print()


ttt.user = ttt.X

board = ttt.initial_state()
# game_over = False
ai_turn = False

while not ttt.terminal(board):
    print_board(board)
    print()

    if not ai_turn:
        input_text = input("Enter your movement (e.g 1,2): ")

        # Excepcion si argumentos invalidos
        player_move = tuple(int(coord) for coord in input_text.split(","))
        valid_moves = ttt.actions(board)
        if player_move not in valid_moves:
            raise Exception("Invalid player movement")

        board = ttt.result(board, player_move)
        ai_turn = True
        continue

    print("Computer thinking ...")
    ai_move = ttt.minimax(board)
    board = ttt.result(board, ai_move)
    ai_turn = False
