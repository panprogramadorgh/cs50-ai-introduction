import csv
import itertools
import sys
import typing

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

# Gene heredity chances based on parent mutated genes and having into account mutation factor
HEREDITY = {
    0: 0 + PROBS["mutation"],
    1: 0.5, # Both probability options have the same chance, so mutation does not affect actually
    2: 1 - PROBS["mutation"]
}

def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def factorizer(iter: typing.Iterable[float]):
    """
    Multiplication function -- equivalent to sum built in function 
    """
    factor = 1
    for n in iter:
        factor *= n
    return factor


def all_sizes_combinations(iter: typing.Iterable[float], r: int):
    iter = list(iter)
    combs = []
    for r in range(len(iter)):
        combs.extend(itertools.combinations(iter, r + 2))
    return combs


def gene_probability(people: dict[str, dict[str, str]], person: str, gene_number: int) -> float:
    """
    Calculates the `gene_number` probability for the given person and people dict

    Args:
        people (dict[str, dict[str, str]]): Dictionary of all individuals.
        person (str): The person name over who calculate probability
        gene_number: The number of mutated genes the person have
    Returns:
        float: The mutated gene probability
    """

    if not 0 <= gene_number <= 2:
        raise ValueError(
            "Invalid gene number. Expected values are 0, 1, or 2. "
            f"Received: {gene_number}."
        )
 
    father = people[person]["father"]
    mother = people[person]["mother"]

    if father is None and mother is None:
        return PROBS["gene"][gene_number]
    if None in (father, mother):
        raise ValueError(
            "Invalid parent specification. "
            "A person must either have both parents specified or neither. "
            f"Person '{person}' has only one parent specified."
        )

    father_gene = gene_probability(people, father, gene_number)
    mother_gene = gene_probability(people, mother, gene_number)

    # P(A) + P(B) - P(A, B)
    return (
        (father_gene * HEREDITY[gene_number]) +
        (mother_gene * HEREDITY[gene_number]) -
        ((father_gene * HEREDITY[gene_number]) * (mother_gene * HEREDITY[gene_number]))
    ) 


def joint_gene_probability(people: dict[str, dict[str, str]], people_set: set[str], gene_number: int) -> float:
    """Calculates joint gene probability over multiple people specified in `people_set`."""

    probability_factor = 1
    for person in people_set:
        probability_factor *= gene_probability(people, person, gene_number)
    return probability_factor


def trait_probability(people: dict[str, dict[str, str]], person: str):
    """Calculates probability for a person to have the trait given `people` dictionary"""

    trait_chances = [] 
    for gene_number in tuple(PROBS["gene"].keys()):
        gene_number_prob = gene_probability(people, person, gene_number)
        trait_prob = PROBS["trait"][gene_number][True] 
        
        # We append each trait probability based on the number of mutated genes
        trait_chances.append(gene_number_prob * trait_prob ) 
        
    # All trait chances subsets (all sizes)
    trait_chances_combinations = all_sizes_combinations(trait_chances, len(PROBS["gene"])) 

    # P(A) + P(B) - P(A, B)
    return sum(trait_chances) - sum([factorizer(comb) for comb in trait_chances_combinations])


def joint_trait_probability(people: dict[str, dict[str, str]], people_set: set[str]):
    """"""

    probability_factor = 1
    for person in tuple(people_set):
        probability_factor *= trait_probability(people, person)
    return probability_factor


def joint_probability(people: dict[str, dict[str, str]], one_gene: set[str], two_genes: set[str], have_trait: set[str]):
    """
    Compute and return the joint probability.

    The probability returned is the probability that:
        - Everyone in `one_gene` has one copy of the gene,
        - Everyone in `two_genes` has two copies of the gene,
        - Everyone not in `one_gene` or `two_genes_set` has no copies of the gene,
        - Everyone in `have_trait` has the trait,
        - Everyone not in `have_trait` does not have the trait.

    Args:
        people (dict[str, dict[str, str]]): Dictionary of all individuals.
        one_gene (set): Set of individuals with one copy of the gene.
        two_genes (set): Set of individuals with two copies of the gene.
        have_trait (set): Set of individuals who have the trait.

    Returns:
        float: The joint probability.
    """

     # Set of all people without the mutated gen
    no_gene = set(people.keys()) - one_gene - two_genes
    have_no_trait = set(people.keys()) - have_trait

    joint = (
        joint_gene_probability(people, no_gene, 0),
        joint_gene_probability(people, one_gene, 1),
        joint_gene_probability(people, two_genes, 2),
        joint_trait_probability(people, have_trait),
        joint_trait_probability(people, have_no_trait)
    )

    return factorizer(joint)

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    print(probabilities, p)    

    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
