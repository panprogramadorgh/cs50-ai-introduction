"""
Tic Tac Toe Player
"""

from typing import Literal, Optional

X = "X"
O = "O"
EMPTY = None

MAX_UTIL = 1
MIN_UTIL = -1
TIE_UTIL = 0

user = None


class Node:
    def __init__(
        self,
        state: list[list[str | None]],
        parent: Optional["Node"],
        action: Optional[tuple[int, int]],
    ):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier: list[Node] = []

    def add(self, node: Node):
        self.frontier.append(node)

    def contains_state(self, state: tuple[int, int]):
        return any(s.state == state for s in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node


class QueueFrontier(StackFrontier):

    def remove(self):
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node


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


def result(board: list[list[str | None]], action):
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

    # FIXME: Crear funcion comparativa de los combos

    players: set[str]
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

    # print(px_board_poses)
    # print(po_board_poses)

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
    v = MIN_UTIL - 1
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board: list[list[str | None]]):
    if terminal(board):
        return utility(board)
    v = MAX_UTIL + 1
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    frontier = QueueFrontier()
    initial_node = Node(board, None, None)
    frontier.add(initial_node)

    p = player(board)

    # Should always be min_value since the player who starts the game is always user and user is the max agent
    value_calculator = max_value if p == user else min_value

    # Should always be MIN_UTIL since the player who starts the game is always user and user is the max agent
    greedy_value = MAX_UTIL if p == user else MIN_UTIL
    ungreedy_value = MAX_UTIL if p != user else MIN_UTIL

    while True:
        if frontier.empty():
            return None

        node = frontier.remove()
        # print(node.action)

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
            v = value_calculator(result(node.state, action))
            node_values[v] = action
            if v == greedy_value:
                break

        # Tie or (just in case not opptimal) action is returned
        next_action = (
            node_values[greedy_value]
            or node_values[TIE_UTIL]
            or node_values[ungreedy_value]
        )
        if next_action is None:
            continue

        next_state = result(node.state, next_action)

        if terminal(next_state):
            return next_action

        frontier.add(Node(state=next_state, parent=node, action=next_action))
