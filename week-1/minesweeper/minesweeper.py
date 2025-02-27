import itertools
import random
import copy


def neighbor_cells(cell: tuple[int, int], width: int, height: int):
    neighbors: set[tuple[int, int]] = set()
    x, y = cell

    left = cell[0] - 1
    right = cell[0] + 1
    top = cell[1] - 1
    bottom = cell[1] + 1

    if x > 0:
        neighbors.add((left, y))
        if y > 0:
            neighbors.add((left, top))
        if y < height - 1:
            neighbors.add((left, bottom))
    if x < width - 1:
        neighbors.add((right, y))
        if y > 0:
            neighbors.add(((right, top)))
        if y < height - 1:
            neighbors.add((right, bottom))
    if y > 0:
        neighbors.add((x, top))
    if y < height - 1:
        neighbors.add((x, bottom))

    return neighbors


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

        self._mines: set[tuple[int, int]] = set()
        self._safes: set[tuple[int, int]] = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def __hash__(self):
        return hash((str(self.cells), self.count))

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self._mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self._safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self._mines.add(cell)
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self._safes.add(cell)
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # Desn't make any sense to check the move in two times
        if cell in self.moves_made:
            return
        
        # Adds the move and makes the cell to be considerated as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Sentence inferences
        inferences: set[Sentence] = set()
        # Neighbor cells relative to current cell's pos
        neighbors = neighbor_cells(cell, self.width, self.height)

        # New sentence is added to knowledge
        s = Sentence(neighbors, count)
        self.knowledge.append(s)

        # Basic inference for all sentences based on count
        # If there is the case in which any of the sentences has no remaining possible mines (the value of count), then it means all associated cells within that sentence aren't mines.
        # For other side, if the number of associated cells is equal to the number of mined cells in that sentence, all cell within must to be mines
        for sentence in copy.deepcopy(self.knowledge):
            if len(sentence.cells) == sentence.count:
                for s_cell in sentence.cells:
                    self.mark_mine(s_cell)
            elif sentence.count == 0:
                for s_cell in sentence.cells:
                    self.mark_safe(s_cell)

        # Make Safe and unsafe cells for all sentences
        # For each safe cell of each sentence makes it safe for the rest of sentences. Same behaviour for mines as for safes.
        for sentence in copy.deepcopy(self.knowledge):
            for mine in sentence.known_mines():
                self.mark_mine(mine)
            for safe in sentence.known_safes():
                self.mark_safe(safe)

        # Removes empty sentences
        # Above inferences may result on empty sentences, to them must be removed from knowledge
        for sentence in copy.deepcopy(self.knowledge):
            if not len(sentence.cells):
                self.knowledge.remove(sentence)

        # Draws extra inference based on sentences relations
        for some_sentence in self.knowledge:
            for other_sentence in self.knowledge:
                # Commmon cells between sentences
                ocurrences: set[tuple[int, int]] = set()
                # Suspicious cell subset
                mines_subset: set[tuple[int, int]] = set()

                # No possible inferences
                if some_sentence.count == other_sentence.count:
                    continue

                # Finds ocurrences between the two sentences
                for s_cell in some_sentence.cells:
                    if s_cell in other_sentence.cells:
                        ocurrences.add(cell)

                # Calculates the mines subset
                if some_sentence.count > other_sentence.count:
                    for s_cell in some_sentence.cells:
                        if s_cell in ocurrences:
                            continue
                        mines_subset.add(s_cell)
                elif other_sentence.count > some_sentence.count:
                    for s_cell in other_sentence.cells:
                        if s_cell in ocurrences:
                            continue
                        mines_subset.add(s_cell)

                # Creates inferred sentence from suspicious subset
                inferred_sentence = Sentence(
                    mines_subset, abs(some_sentence.count - other_sentence.count)
                )
                inferences.add(inferred_sentence)


        # Draws extra inference based on sentences relations
        # for sentence in self.knowledge:
        #     # Commmon cells between sentences
        #     ocurrences: set[tuple[int, int]] = set()
        #     # Suspicious cell subset
        #     mines_subset: set[tuple[int, int]] = set()

        #     # No possible inferences
        #     if s.count == sentence.count:
        #         continue

        #     # Finds ocurrences between the two sentences
        #     for s_cell in sentence.cells:
        #         if s_cell in s.cells:
        #             ocurrences.add(cell)

        #     # Calculates the mines subset
        #     if sentence.count > s.count:
        #         for s_cell in sentence.cells:
        #             if s_cell in ocurrences:
        #                 continue
        #             mines_subset.add(s_cell)
        #     elif s.count > sentence.count:
        #         for s_cell in s.cells:
        #             if s_cell in ocurrences:
        #                 continue
        #             mines_subset.add(s_cell)

        #     # Creates inferred sentence from suspicious subset
        #     inferred_sentence = Sentence(
        #         mines_subset, abs(sentence.count - s.count)
        #     )

        #     inferences.add(inferred_sentence)

        # Appends all infereces found
        for inferred in inferences:
            self.knowledge.append(inferred)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
          
        best_move = [8, None]

        # If there are available safe moves, then pick one that weren't choosed before
        safe_moves: tuple[tuple[int, int]] = tuple(move for move in self.safes if move not in self.moves_made) 
        if len(safe_moves) > 0:
            best_move[0] = 0
            best_move[1] = safe_moves[random.randint(0, len(safe_moves) - 1)]
            print("safe move ", end="")

        # Otherwise take the less risky option -- which may result eventually result losing the game
        for sentence in self.knowledge:
            if sentence.count >= best_move[0]:
                continue
            best_move[0] = sentence.count
            best_move[1] = copy.deepcopy(sentence.cells).pop()
            print("maybe safe move ", end="")

        print(best_move[1])
        return best_move[1]

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        available: list[tuple[int, int]] = list()
        for i in range(self.width):
            for j in range(self.height):
                move = (i, j)
                if move not in self.moves_made and move not in self.mines:
                    available.append(move)

        # No available and not mined cells are free
        if len(available) == 0:
            return None

        # Random cell, may contain mine
        random_move = available[random.randint(0, len(available) - 1)]
        print("random movement", random_move)
        return random_move
