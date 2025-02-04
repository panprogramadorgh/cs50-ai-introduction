from typing import Optional


class Node:
    """Data structure that allows to represent states. In this particular problem, the node state is a person id."""

    def __init__(
        self, state: Optional["int"], parent: Optional["Node"], action: Optional["int"]
    ):
        # Represents current node person's id
        self.state = state
        # Represents parnet node person's id
        self.parent = parent
        # Represents performed action by self.parent
        self.action = action

    # Makes it compatible with data structures like sets (that internally uses hashes to store objets)
    def __hash__(self):
        return hash((self.state, self.action))


class StackFrontier:
    def __init__(self):
        self.frontier: list[Node] = []

    def add(self, node: Node):
        self.frontier.append(node)

    def contains_state(self, state: int):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
