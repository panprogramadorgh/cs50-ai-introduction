"""
Tic Tac Toe Player
"""

import math
from typing import Literal
from runner import user

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board: list[list[str | None]]):
    """
    Returns player who has the next turn on a board.
    """
    opponent = user if user == X else O
    px_tokens, po_tokens = 0, 0

    for row in board:
        px_tokens += row.count(X)
        po_tokens += row.count(O)

    return user if px_tokens == po_tokens else opponent


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possibilities = []
    for i in range(3):
        for j in range(3):
            if board[i][j] is not None:
                possibilities.append((i, j))

    return possibilities


def result(board: list[list[str | None]], action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    boardcpy = board.copy()
    i, j = action
    p = player(boardcpy)
    boardcpy[i][j] = p
    return boardcpy


def locate_player_poses(board: list[list[str | None]], player: Literal["X", "O"]):
    """
    Returns a copy of board, but quite different. Player positions are represented with True and void or other's player positions with False.
    """

    board_poses: list[tuple[bool, bool, bool]] = []
    for row in board:
        row_poses = (X == token for token in row)
        board_poses.append(row_poses)
    
    return tuple(board_poses)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    winner_combos = (
        ((True, True, True), (False, False, False), (False, False, False)),
        ((False, False, False), (True, True, True), (False, False, False)),
        ((False, False, False), (False, False, False), (True, True, True)),
        ((True, False, False), (True, False, False), (True, False, False)),
        ((False, True, False), (False, True, False), (False, True, False)),
        ((False, False, True), (False, False, True), (False, False, True)),
        ((True, False, False), (False, True, False), (False, False, True)),
        ((False, False, True), (False, True, False), (True, False, False)),
    )

    # Locates player's tokens positions
    px_board_poses = locate_player_poses(board, X)
    po_board_poses = locate_player_poses(board, O)

    # Checks for combos ocurrences
    px_is_winner = (
        X if any(combo == tuple(px_board_poses) for combo in winner_combos) else None
    )
    po_is_winner = (
        O if any(combo == tuple(po_board_poses) for combo in winner_combos) else None
    )

    return px_is_winner or po_is_winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    board_is_full = True
    for row in board:
        board_is_full = None not in row
        if not board_is_full: break
    
    return board_is_full or (winner(board) is not None)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    opts = { X: 1, O: -1, None: 0 }
    return opts[winner(board)]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
