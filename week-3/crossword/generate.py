import sys

from crossword import *
from util import *

class CrosswordCreator:

    def __init__(self, crossword: Crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
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
                self.domains[var].remove(word)

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

        # Absolute position for variable overlap
        (i, j) = overlap

        # Absolute J - variable's relative J, or
        # Absolute I - variable's relative I
        x_overlap_index = j - x.j if x.direction == Variable.ACROSS else i - x.i
        y_overlap_index = j - y.j if x.direction == Variable.ACROSS else i - y.i

        # We copy the set structure since we are going to remove elements at the same time we iterate through
        x_domain = self.domains[x].copy()

        # X domain was revised
        revised = False

        for x_value in x_domain:
            # We iterate for each value of `y` to find a compatible value with `x`
            compatible_value = False
            for y_value in self.domains[y]:
                if x_value[x_overlap_index] != y_value[y_overlap_index]:
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

        # If arcs isn't specified, then take all variable overlaps as arcs
        problem_arcs = self.crossword.overlaps.keys() if arcs is None else arcs

        while len(problem_arcs) > 0:
            (x, y) = problem_arcs.pop(0)
            if self.revise(x, y):  # Reduces x's domain if needed to enfoce consistency
                # Seme variable's domain has no values and thus there's no solution to the csp
                if len(self.domains[x]) == 0:
                    return False

                # If some values from x's domain were ruled out, then check arc consistency for each neighbor of x except of y
                for z in self.crossword.neighbors(x):
                    if z == y:
                        continue
                    problem_arcs.append((x, y))
        return True

    def assignment_complete(self, assignment: dict[Variable, str]):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # We are going to assume assignment does not contain a key for all possible variables in the problem so we need check if that variable exists in assignment and thus confirm it is complete.

        is_complete = True
        for variable in self.crossword.variables:
            if has_key(variable, assignment):
                continue
            is_complete = False
            break
        return is_complete

    def consistent(self, assignment: dict[Variable, str]):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        assignment_words = tuple(word for word in assignment.values())

        # Dupplicated words isn't allowed
        if len(set(assignment_words)) != len(assignment_words):
            return False

        # Ruling out domain values from variables
        # Each variable has to fit in in terms of length
        self.enforce_node_consistency()
        # Each variable has to correctly overlap with other variables
        self.ac3()

        # Checking if the csp has a solution
        for variable in self.crossword.variables:
            if len(self.domains[variable]) == 0:
                return False

        return True

    def order_domain_values(self, var: Variable, assignment: dict[Variable, str]):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Calculates the sumation of all variable's domain size
        domains_len = lambda dom: sum(tuple(len(dom[neihgbour]) for neihgbour in neighbours))
        
        # A copy of the original self.domains dict (so then we can modify and test other possible domains)
        current_domains = self.domains.copy()  
        
        # Sumation of all variable's domain size  
        current_domains_len = domains_len(current_domains)

        # Neighbouring variables
        neighbours = self.crossword.neighbors(var)
    
        # We assume assignment is going to be provided as consistent (all variables in var's domain should return True when self.consistent)
        # In any case, all no consistent variables will belong to this set and thus them will be queued at the end the list returned by this function.
        no_consistent: set[Variable] = {}

        # Contains the number or discarted values for neighbouring variables
        all_domains_len: dict[str, int] = {}

        for value in self.domains[var]:
            self.domains = current_domains.copy()
            self.domains[var] = {value}
            if not self.consistent():
                no_consistent.add(value)
                break
            all_domains_len[value] = current_domains_len - domains_len(self.domains)
    
        sorted_domains_len = [pair[1] for pair in quick_sort(list(all_domains_len.items()), get_value=lambda pair: pair[1], dir=ASC_SORT)]

        return sorted_domains_len

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


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
