from typing import Optional


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