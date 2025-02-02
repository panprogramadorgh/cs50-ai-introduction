from enum import Enum, auto
from sys import argv


class Actions(Enum):
    up = auto()
    down = auto()
    left = auto()
    right = auto()


class Vec2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_tuple(self):
        return (self.x, self.y)

    def __str__(self):
        return f"""
		{self.get_tuple()}
		""".strip()


class NodeBase:
    def __init__(self, state: Vec2, action: Actions):
        self.state = state
        self.action = action


class Node(NodeBase):
    def __init__(self, state, parent, action):
        super().__init__(state=state, action=action)
        self.parent = parent

    def __str__(self):
        return f"""
{"-" * 10}
state\t{self.state}
parent\t{self.parent}
action\t{self.action}
{"-" * 10}\n"""


class Solution:
    def __init__(
        self, node: Node, actions: list[Actions], cells: list[Vec2], num_explored: int
    ):
        self.node = node
        self.actions = actions
        self.cells = cells
        self.num_explored = num_explored


class StackFrontier:
    def __init__(self):
        self.frontier: list[Node] = []

    def add(self, node: Node):
        self.frontier.append(node)

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")

        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node

    def empty(self):
        return len(self.frontier) == 0

    def contains_state(self, state: Vec2):
        return any(node.state.get_tuple == state.get_tuple() for node in self.frontier)


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")

        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node


class Maze:
    def __init__(self, filename: str, frontier=StackFrontier):
        with open(filename) as f:
            contents = f.read()
        self.filecheck(contents)

        self.frontier_class = frontier

        lines = contents.splitlines()
        self.height = len(lines)
        self.width = len(lines[0])

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    slot = lines[i][j]
                    if slot == "A":
                        self.start = Vec2(j, i)
                        row.append(False)
                    elif slot == "B":
                        self.goal = Vec2(j, i)
                        row.append(False)
                    elif slot == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(True)
            self.walls.append(row)

        self.solution = None

    def filecheck(self, contents: str):
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one stat point")
        elif contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        lines = contents.splitlines()
        if len(lines) == 0:
            raise Exception("must must have one line of height atleast")

        if any(line for line in lines if len(line) != len(lines[0])):
            raise Exception("maze lines must have exactly the same width")

    def print(self, node: Node):
        prev_states: list[Vec2] = []
        while node.parent != None:
            prev_states.append(node.state)
            node = node.parent

        for i in range(self.height):
            for j in range(self.width):
                slot = self.walls[i][j]
                if slot:
                    print("#", end="")
                elif (j, i) == self.start.get_tuple():
                    print("A", end="")
                elif (j, i) == self.goal.get_tuple():
                    print("B", end="")
                elif any(s.get_tuple() == (j, i) for s in prev_states):
                    print("*", end="")
                else:
                    print(" ", end="")
            print()

    def neighbors(self, state: Vec2):
        col, row = state.get_tuple()
        action_candidates = (
            (Actions.up, Vec2(col - 1, row)),
            (Actions.down, Vec2(col + 1, row)),
            (Actions.left, Vec2(col, row - 1)),
            (Actions.right, Vec2(col, row + 1)),
        )

        result: list[NodeBase] = []
        for action, state in action_candidates:
            col, row = state.get_tuple()
            if (
                0 <= row < self.height
                and 0 <= col < self.width
                and self.walls[row][col] == False
            ):
                node_base = NodeBase(state=state, action=action)
                result.append(node_base)
        return result

    def solve(self):
        """Solves the meze, if it is possible"""

        start = Node(state=self.start, parent=None, action=None)
        frontier = self.frontier_class()
        frontier.add(start)

        self.explored = set()
        num_explored = 0

        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            num_explored += 1

            if node.state.get_tuple() == self.goal.get_tuple():
                actions = []
                cells = []
                solution_node = node
                while node.parent is not None:
                    actions.insert(0, node.action)
                    cells.insert(0, node.state)
                    node = node.parent

                self.solution = Solution(
                    node=solution_node,
                    actions=actions,
                    cells=cells,
                    num_explored=num_explored,
                )
                return

            self.explored.add(node.state.get_tuple())
            neighbor_nodes = self.neighbors(node.state)
            for n in neighbor_nodes:
                if (
                    not frontier.contains_state(n.state)
                    and n.state.get_tuple() not in self.explored
                ):
                    frontier.add(Node(state=n.state, parent=node, action=n.action))


def main():
    if len(argv) != 2:
        raise Exception(f"Usage: python3 {argv[0]} maze.txt")

    maze = Maze(argv[1], QueueFrontier)
    maze.solve()

    maze.print(maze.solution.node)
    print(maze.solution.num_explored)

    pass


if __name__ == "__main__":
    main()
