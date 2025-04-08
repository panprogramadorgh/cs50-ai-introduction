import sys
from crossword import *
from typing import Any


# FIXME: Parece haber un problema con las direcciones al momento de imprimir las variables


DESC_SORT, ASC_SORT = 0, 1
"""quick_sort dir constant values"""


def quick_sort(
    iter: list[Any],
    left: int = 0,
    right: int = None,
    dir: int = ASC_SORT,  # DESC_SORT | ASC_SORT
    sort=lambda x: x,
):
    """
    ### QuickSort algorithm

    - Declare a `i` variable which will be the next pivot pos and will have an initial value of 0

    - Iterates for each `iter` value

    - For each iteration, if `value` is less than the current pivot value, then swap the value at next pivot pos by the iteration `value`
    """

    # Helper function
    compare = lambda x, y: (x <= y) if (dir == ASC_SORT) else (x >= y)

    if right is None:
        right = len(iter) - 1

    if left >= right:
        return iter

    pivot = sort(iter[right])  # Current pivot value
    i = left  # Next pivot index

    for j in range(left, right):
        if compare(sort(iter[j]), pivot):
            iter[i], iter[j] = iter[j], iter[i]
            i += 1

    iter[i], iter[right] = iter[right], iter[i]

    quick_sort(iter, left=left, right=i - 1, sort=sort, dir=dir)
    quick_sort(iter, left=i + 1, right=right, sort=sort, dir=dir)

    return iter


class CrosswordCreator:

    def __init__(self, crossword: Crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment: dict[tuple[Variable, str]]):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for var in self.crossword.variables:
            for word in self.crossword.words:
                if len(word) == var.length:
                    continue
                self.domains[var].discard(word)

    def revise(self, x: Variable, y: Variable):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # Variable overlap
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:  # No overlap means no arcs between
            return False

        # Each overlap consists of a tuple with the position at the variable's cells list
        (i, j) = overlap

        x_domain = self.domains[x].copy()

        # X domain was revised
        revised = False

        for x_value in x_domain:
            # We iterate for each value of `y` to find a compatible value with `x`
            compatible_value = False
            for y_value in self.domains[y]:
                if x_value[i] != y_value[j]:
                    continue
                compatible_value = True
                break
            if compatible_value:
                continue

            # If isn't compatible we remove the value from its domain
            self.domains[x].remove(x_value)
            revised = True

        return revised

    def ac3(self, arcs: list[tuple[Variable, Variable]] | None = None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # This function works over the assumption that each variable overlap of the form x, y has no difference with y, x.

        # If arcs isn't specified, then take all variable overlaps as arcs
        arcs = arcs if arcs is not None else self.crossword.overlaps.keys()
        # filtered_arcs
        farcs = [arc for arc in arcs if self.crossword.overlaps[arc] is not None]
        # unordered_filtered_arcs
        # ufarcs = [set(arc) for arc in farcs]

        queue = farcs.copy()
        while len(queue) > 0:
            (x, y) = queue.pop(0)
            if self.revise(x, y):  # Reduces x's domain if needed to enfoce consistency
                # Seem variable's domain has no values and thus there's no solution to the csp
                if len(self.domains[x]) == 0:
                    return False

                # If some values from x's domain were ruled out, then check arc consistency for each neighbor of x except of y and those that doesn't belong to `arcs`.
                for z in self.crossword.neighbors(x):
                    if z == y or (z, x) not in farcs:
                        continue
                    queue.append((x, z))
        return True

    def enforce_consistency(self, assignment: dict[Variable, str] = {}):
        """
        Searches for both arc and node consistency by reducing each csp variables domain — having into account fixed the values from `assignment`.

        If there is no solution to the csp since some variable got zero elements in its domain and thus there is no solution to the problem it returns False, otherwise (i.e we still need to find a solution but we atleast know that there might be one) return True.
        """

        # Ruling out inconsistent values from variable domains

        self.enforce_node_consistency()
        for var in self.crossword.variables:
            if len(self.domains[var]):
                continue
            return False

        # Valid overlaps are the only chosen
        overlaps: list[tuple[Variable, Variable]] = [
            overlap
            for (overlap, pos) in self.crossword.overlaps.items()
            if pos is not None
        ]

        arcs: list[tuple[Variable, Variable]] = None
        if len(assignment):
            arcs = []
            for x, y in overlaps:
                if x in assignment.keys() and y in assignment.keys():
                    continue
                arcs.append((x, y))
        return self.ac3(arcs)

    def assignment_complete(self, assignment: dict[Variable, str]):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # We are going to assume assignment does not contain a key for all possible variables in the problem so we need check if that variable exists in assignment and thus confirm it is complete.

        is_complete = True
        for variable in self.crossword.variables:
            if variable in assignment.keys():
                continue
            is_complete = False
            break
        return is_complete

    def consistent(self, assignment: dict[Variable, str]):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # We copy the current self.domains dict so after checking for consistency we can restore i
        current_domains = self.domains.copy()

        # Dupplicated words are not allowed
        assignment_words = tuple(word for word in assignment.values())
        if len(set(assignment_words)) != len(assignment_words):
            return False

        if not self.enforce_consistency(assignment):
            self.domains = current_domains
            return False

        self.domains = current_domains
        return True

    def order_domain_values(self, var: Variable, assignment: dict[Variable, str]):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Optimize: In order to sort by the less restrective value for var, we have to create multiple versions of self.domains with the slightly difference of var's domain.

        # Calculates the sumation of all variable's domain size
        domains_len = lambda: sum(
            len(self.domains[neighbour]) for neighbour in self.crossword.neighbors(var)
        )

        # A copy of the original self.domains dict (so then we can modify and test other possible domains)
        current_domains = self.domains.copy()  # <- do not modify

        # Sumation of all variable's domain size
        current_domains_len = domains_len()

        # We assume assignment is going to be provided as consistent (all variables in var's domain should return True when self.consistent)

        # In any case, all no consistent variables will belong to this set and thus them will be queued at the end the list returned by this function.
        no_consistent: set[Variable] = set()

        # Contains the number or discarted values for neighbouring variables
        all_domains_len: dict[str, int] = {}

        for value in current_domains[var]:
            self.domains = current_domains.copy()
            self.domains[var] = {value}

            if not self.enforce_consistency(assignment):
                no_consistent.add(var)
                continue

            all_domains_len[value] = current_domains_len - domains_len()

        self.domains = current_domains

        sorted_domains_len = quick_sort(
            list(all_domains_len.items()),
            sort=lambda pair: pair[1],
            dir=ASC_SORT,
        )

        sorted_vars = [pair[0] for pair in sorted_domains_len] + list(no_consistent)

        return sorted_vars

    def select_unassigned_variable(self, assignment: dict[Variable, str]):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        if self.assignment_complete(assignment):
            raise ValueError("no unassigned values remaining in assignment")

        # Unassigned variables, its domain len (remaining values), its degree (number of neighbours)
        unassigned: list[tuple[Variable, int, int]] = []

        for var in self.domains.keys():
            if var in assignment.keys() or not len(self.domains[var]):
                continue

            unassigned.append(
                (
                    var,  # Variable - 0
                    len(self.domains[var]),  # Variable's domain len - 1
                    len(self.crossword.neighbors(var)),  # Variable's degree len - 2
                )
            )

        # minimum remaining values y max degree sorting
        sorted_unassigned = quick_sort(
            quick_sort(unassigned, sort=lambda pair: pair[1], dir=ASC_SORT),
            sort=lambda pair: pair[2],
            dir=DESC_SORT,
        )

        return sorted_unassigned[0][0]

    def backtrack(self, assignment: dict[Variable, str]):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        # Selected variable
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            next_assignment = assignment.copy()
            next_assignment[var] = value
            if self.consistent(next_assignment):
                final_assignment = self.backtrack(next_assignment)
                if final_assignment is not None:
                    return final_assignment

        return None  # Backtracks


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
