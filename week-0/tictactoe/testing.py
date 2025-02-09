import tictactoe as ttt

# Testing and debugging file

ttt.user = ttt.X
ia = ttt.O if ttt.user == ttt.X else ttt.X

board = ttt.initial_state()
player = ttt.user

while not ttt.terminal(board):
    ttt.print_state(board)
    print()

    if player == ttt.user:
        input_text = input("Enter your movement (e.g 1,2): ")

        # Excepcion si argumentos invalidos
        player_move = tuple(int(coord) for coord in input_text.split(","))
        valid_moves = ttt.actions(board)
        if player_move not in valid_moves:
            raise Exception("Invalid player movement")

        board = ttt.result(board, player_move)
        player = ia
        continue

    print("Computer thinking ...")
    ai_move = ttt.minimax(board)
    board = ttt.result(board, ai_move)
    player = ttt.user

print("Game Over")
print("Player", ttt.winner(board), "has wone")
