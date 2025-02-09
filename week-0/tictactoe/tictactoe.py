"""
Tic Tac Toe Player
"""

from typing import Literal

X = "X"
O = "O"
EMPTY = None

MAX_UTIL = 1
MIN_UTIL = -1
TIE_UTIL = 0

user = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def print_state(board: list[list[str | None]], end=""):
    for row in board:
        for token in row:
            print(token + " " if token is not None else "· ", end="")
        print()
    print(end)


def player(board: list[list[str | None]]):
    """
    Returns player who has the next turn on a board.
    """
    opponent = O if user == X else X
    px_tokens, po_tokens = 0, 0

    for row in board:
        px_tokens += row.count(X)
        po_tokens += row.count(O)

    return user if px_tokens == po_tokens else opponent


def actions(board: list[list[str | None]]):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possibilities: list[tuple[int, int]] = []
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                possibilities.append((i, j))

    return possibilities


def result(board: list[list[str | None]], action: tuple[int, int]):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Deep bidimensional list copy
    boardcpy = [[token for token in row] for row in board]
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
        row_poses = tuple(player == token for token in row)
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

    for combo in winner_combos:
        players = {X, O}
        for i in range(3):
            for j in range(3):
                if not combo[i][j]:
                    continue
                if not px_board_poses[i][j]:
                    players.discard(X)
                if not po_board_poses[i][j]:
                    players.discard(O)
        if len(players) == 1:
            return players.pop()  # The only token is the winner

    # If both players win (illigal board), then return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    board_is_full = True
    for row in board:
        board_is_full = None not in row
        if not board_is_full:
            break

    return board_is_full or (winner(board) is not None)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    opts = {X: MAX_UTIL, O: MIN_UTIL, None: TIE_UTIL}
    return opts[winner(board)]


# TODO: Obtimize with Apha-Beta Prunning


def max_value(board: list[list[str | None]]):
    if terminal(board):
        return utility(board)
    v = -float("inf")
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board: list[list[str | None]]):
    if terminal(board):
        return utility(board)
    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # No game winner
    if terminal(board):
        return None

    # The current user
    p = player(board)
    best_action = None

    # It is the turn of the opponent because the last movement is made by user
    if p == user:
        best_value = -float("inf")
        for action in actions(board):
            v = min_value(result(board, action))
            if v < best_value:
                best_value = v
                best_action = action
    else:
        best_value = float("inf")
        best_action = None
        for action in actions(board):
            v = max_value(result(board, action))
            if v < best_value:
                best_value = v
                best_action = action

    return best_action
