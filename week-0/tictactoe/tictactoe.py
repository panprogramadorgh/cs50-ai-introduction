"""
Tic Tac Toe Player
"""

from typing import Literal
from runner import user
from util import QueueFrontier, Node

X = "X"
O = "O"
EMPTY = None

MAX_UTIL = 1
MIN_UTIL = -1
TIE_UTIL = 0


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
    v = -2
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board: list[list[str | None]]):
    if terminal(board):
        return utility(board)
    v = 2
    for action in actions(board):
        v = min(v, max_value(board, action))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    frontier = QueueFrontier()
    initial_node = Node(board, None, None)
    frontier.add(initial_node)

    while True:
        if frontier.empty():
            return None

        node = frontier.remove()

        # Implementar optimizacion Alpha-Beta Prunning
        # Se almacenan los valores para los nodos hermanos.
        # Para saber los nodos son hermanos, tienen que
        # depender directamente del mismo nodo.
        # Los nodos hijos de cada hermano seran introducidos al frontier
        # (seran descubiertos posteriormente)
        # solamente en caso de que su valor utility sea
        # superior al valor del nodo hermano mas alto,
        # de lo contrario no agregaremos dicho nodo porque
        # incluira un nodo hijo con un valor demasiado pequeño
        # y potencialmente elegible por el agente min (si juega
        # optimamente)

        node_values: dict[int, tuple[int, int] | None] = {
            MAX_UTIL: None,
            MIN_UTIL: None,
            TIE_UTIL: None,
        }
        for action in actions(node.state):
            v = max_value(result(node, action))
            node_values[v] = action
            if v == 1:
                break

        # Tie or (just in case not opptimal) action is returned
        next_action = (
            node_values[MAX_UTIL] or node_values[TIE_UTIL] or node_values[MIN_UTIL]
        )
        next_state = result(node.state, next_action)

        if terminal(next_state):
            return next_action

        frontier.add(Node(state=next_state, parent=node, action=next_action))
