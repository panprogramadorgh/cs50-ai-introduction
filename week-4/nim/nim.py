import sys
import numpy as np
from numpy.typing import NDArray
import random
import time
from typing import Callable, Any, Literal, Optional


class Nim:

    def __init__(self, initial=[1, 3, 5, 7]):
        """
        Initialize game board.
        Each game board has
            - `piles`: a list of how many elements remain in each pile
            - `player`: 0 or 1 to indicate which player's turn
            - `winner`: None, 0, or 1 to indicate who the winner is
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles: list[int]) -> set[tuple[int, int]]:
        """
        Nim.available_actions(piles) takes a `piles` list as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of removing `j` items
        from pile `i` (where piles are 0-indexed).
        """
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Nim.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    @classmethod
    def move_state(cls, state: list[int], action: tuple[int, int]):
        """
        Moves the provided state given the action.
        """

        pile, count = action

        if pile < 0 or pile >= len(state):
            raise ValueError("Invalid pile")
        elif count < 1 or count > state[pile]:
            raise ValueError("Invalid number of objects")

        state[pile] -= count
        return state

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action: tuple[int, int]):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        if self.winner is not None:
            raise Exception("Game already won")
        self.move_state(self.piles, action)
        self.switch_player()
        if all(p == 0 for p in self.piles):
            self.winner = self.player

    # Default move method for this exercise, since we are enhancing the model we will make use of a different one
    def _move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count
        self.switch_player()

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI:

    QReader = Literal["shallow", "lookahead"]

    @property
    def q_readers(
        self,
    ) -> dict[QReader, Callable[[list[int], tuple[int, int], dict], float]]:
        return {
            "shallow": lambda state, action, kwargs: self.get_q_value(
                state, action, **kwargs
            ),
            "lookahead": lambda state, action, kwargs: self.lookahead(
                state, action, **kwargs
            ),
        }

    """
    Built in self.q readers.
    """

    # ---

    def __init__(
        self,
        model_name: str,
        alpha: float = 0.25,
        epsilon: float = 0.2,
        lookahead_depth: int = 6,
    ):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """

        self.model_name = model_name
        self.q: dict[tuple[tuple[int, ...], tuple[int, int]], float] = dict()
        self.alpha = alpha
        self.epsilon = epsilon
        self.lookahead_depth = lookahead_depth

    def get_q_value(self, state: list[int], action: tuple[int, int]) -> float:
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        q_key = (tuple(state), action)
        q_value = self.q.get(q_key)
        return 0 if q_value is None else q_value

    def lookahead(
        self, state: list[int], _unused, max_depth: int, _acc: float = 0
    ) -> float:
        """
        Recursively advances future states by choosing the grediest and accumulates rewards to verify the "quality" of the path.
        """
        greedy = self.get_greedy(state)
        q, a = 0, 1  # Clarified access

        if max_depth <= 0 or greedy is None:
            return _acc

        _acc += greedy[q]

        if max_depth <= 0 or greedy[a] is None:
            return _acc

        Nim.move_state(state, greedy[a])
        return self.lookahead(state, _unused, max_depth - 1, _acc)

    def update(
        self,
        old_state: list[int],
        action: tuple[int, int],
        new_state: list[int],
        reward: int,
    ):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_greedy(
        self,
        state: list[int],
        q_reader: QReader = "shallow",
        **kwargs,  # Reader arguments
    ):
        """
        Returns the immediate greadiest (q, action) for the current state.
        """
        if q_reader not in self.q_readers.keys():
            raise ValueError(f"Invalid q_reader: 'f{q_reader}'")
        q_reader_cb = self.q_readers[q_reader]

        # If no actions available, return None
        actions = Nim.available_actions(state)
        if not len(actions):
            return None

        # We initially take one action randomly to be the best one
        best: tuple[float, tuple[int, int]] = (0.0, random.choice(tuple(actions)))
        for a in actions:
            # DEBUG: We try using get_q_value directly, instead of by modular readers
            q_value = q_reader_cb(state.copy(), a, kwargs)

            if q_value > best[0]:
                best = (q_value, a)
        return best

    def update_q_value(
        self,
        state: list[int],
        action: tuple[int, int],
        old_q: float,
        reward: int,
        future_rewards: float,
    ):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        q_key = (tuple(state), action)
        self.q[q_key] = old_q + (self.alpha * (reward + future_rewards - old_q))

    def best_future_reward(self, state: list[int]):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """

        # If no available actions are found (for instance the game is gone), None will be return and we will reciebe an error.

        best_lookahead = self.get_greedy(
            state, q_reader="lookahead", max_depth=self.lookahead_depth
        )

        return best_lookahead[0] if best_lookahead is not None else 0.0

    def choose_action(self, state: list[int], epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """

        actions = Nim.available_actions(state)

        if not len(actions):
            return None
        elif epsilon and random.random() <= self.epsilon:
            return random.choice(tuple(actions))

        return self.get_greedy(
            state, q_reader="lookahead", max_depth=self.lookahead_depth
        )[1]


def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = NimAI(f"model_trained_{n}_times")

    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()

        # Keep track of last move made by either player
        last = {0: {"state": None, "action": None}, 1: {"state": None, "action": None}}

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1,
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0,
                )

    print("Done training")

    # Return the trained AI
    return player


def play(ai: NimAI, human_player=None):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim()

    # Game loop
    while True:

        # Print contents of piles
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()

        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Let human make a move
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI make a move
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Make move
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return


def ai_confrontation(models: list[NimAI]):
    if len(models) != 2:
        raise ValueError("Expected models: 2")
    if random.random() < 0.5:
        models = (models[1], models[0])

    game = Nim()

    while game.winner is None:
        choice: tuple[int, int] = models[game.player].choose_action(
            game.piles, epsilon=False
        )
        game.move(choice)

    winner = models[game.winner]
    return winner
