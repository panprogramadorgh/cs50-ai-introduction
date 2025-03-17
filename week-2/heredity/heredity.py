import csv
import itertools
import sys
import typing

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}

# Gene heredity chances based on parent mutated genes and having into account mutation factor
HEREDITY = {
    0: 0 + PROBS["mutation"],
    1: 0.5,  # Both probability options have the same chance, so mutation does not affect actually
    2: 1 - PROBS["mutation"],
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
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
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False if row["trait"] == "0" else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
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


def pass_gene(distribution: tuple[float, float, float]) -> float:
    """
    Returns the probability that a person will transmit the mutated gene to their child given their gene number probability distribution.

    Args:
        distribution (tuple[float, float, float]): Consists in a three positions tuple, each of one corresponging to the probability of a determinated number of genes.

        ```python
        no_genes = 0.96
        one_gene = 0.03
        two_genes = 0.01

        person_distribution = (no_genes, one_gene, two_genes)
        p = pass_gene(person_distribution)
        ```
    Returns:
        float: The probability given the probability `distribution`
    """

    chances_to_pass = (
        distribution[0] * HEREDITY[0],
        distribution[1] * HEREDITY[1],
        distribution[2] * HEREDITY[2],
    )

    combinations = tuple(tuple(comb) for comb in powerset(chances_to_pass) if len(comb) > 1)

    return sum(chances_to_pass) - sum(tuple(factorizer(comb) for comb in combinations))


def gene_dist(
    people: dict[str, dict[str, str]], person: str
) -> tuple[float, float, float]:
    """
    Calculates the `gene_number` probability distribution for the given person and people dict

    Args:
        people (dict[str, dict[str, str]]): Dictionary of all individuals.
        person (str): The person name over who calculate probability
        gene_number: The number of mutated genes the person have
    Returns:
        tuple[float, float, float]: no genes probability, one gene probability, two genes probability
    """

    father = people[person]["father"]
    mother = people[person]["mother"]

    if father is None and mother is None:
        # Unconditional gene probability distribution
        return (PROBS["gene"][0], PROBS["gene"][1], PROBS["gene"][2])

    if None in (father, mother):
        raise ValueError(
            "Invalid parent specification. "
            "A person must either have both parents specified or neither. "
            f"Person '{person}' has only one parent specified."
        )

    father_dist = gene_dist(people, father)
    mother_dist = gene_dist(people, mother)
    chances_to_pass = (pass_gene(father_dist), pass_gene(mother_dist))

    return (
        1 - sum(chances_to_pass),
        sum(chances_to_pass) - factorizer(chances_to_pass),
        factorizer(chances_to_pass),
    )


def gene(people: dict[str, dict[str, str]], person: str, gene_number):
    """Returns the probability of gene_number in person"""
    return gene_dist(people, person)[gene_number]


def joint_gene(
    people: dict[str, dict[str, str]], people_set: set[str], gene_number: int
) -> float:
    """Calculates joint gene probability over multiple people specified in `people_set`."""

    probability_factor = 1
    for person in people_set:
        probability_factor *= gene(people, person, gene_number)
    return probability_factor


def trait(people: dict[str, dict[str, str]], person: str):
    """Calculates probability for a person to have the trait given `people` dictionary"""
    # Gene probability distribution for person
    # tuple[float, float, float]
    # (no_genes, one_gene, two_genes)
    dist = gene_dist(people, person)

    # Trait chances (based of gene number)
    trait_chances = (
        dist[0] * PROBS["trait"][0][True],
        dist[1] * PROBS["trait"][1][True],
        dist[2] * PROBS["trait"][2][True],
    )

    # All trait chances subsets (all sizes)
    combinations = tuple(tuple(comb) for comb in powerset(trait_chances) if len(comb) > 1)

    # P(A) + P(B) - P(A, B)
    return sum(trait_chances) - sum(tuple(factorizer(comb) for comb in combinations))


def joint_trait(
    people: dict[str, dict[str, str]], people_set: set[str], no_trait: bool = False
):
    """Returns the joint probability for a set of people to have the hearing trait.

    Args:
        people (dict[str, dict[str, str]]): Inheritance relationships

        people_set (set[str]): Set of people from to calculate the probability that they have the trait

        no_trait (bool): Inverts the probability calculation so the function will return the probability por `people_set` to do not have the trait

    Returns:
        float: The probability factor given `people_set` and `no_trait`
    """

    probability_factor = 1
    for person in tuple(people_set):
        if no_trait:
            probability_factor *= 1 - trait(people, person)
        else:  
            probability_factor *= trait(people, person)
    return probability_factor


def joint_probability(
    people: dict[str, dict[str, str]],
    one_gene: set[str],
    two_genes: set[str],
    have_trait: set[str],
):
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
        joint_gene(people, no_gene, 0),
        joint_gene(people, one_gene, 1),
        joint_gene(people, two_genes, 2),
        joint_trait(people, have_trait),
        joint_trait(people, have_no_trait, no_trait=True),
    )

    return factorizer(joint)


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # Lefting people
    no_gene = set(probabilities.keys()) - one_gene - two_genes
    have_no_trait = set(probabilities.keys()) - have_trait

    for person in no_gene:
        probabilities[person]["gene"][0] += p

    for person in one_gene:
        probabilities[person]["gene"][1] += p

    for person in two_genes:
        probabilities[person]["gene"][2] += p

    for person in have_trait:
        probabilities[person]["trait"][True] += p

    for person in have_no_trait:
        probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in tuple(probabilities.keys()):
        gene_dist_sum = sum(probabilities[person]["gene"].values())
        trait_dist_sum = sum(probabilities[person]["trait"].values())

        # If the whole distribution sums 0, then any normalizer value will be choosen (1 in this case)
        gene_normalizer = trait_normalizer = 1
        if gene_dist_sum:
            gene_normalizer = 1 / gene_dist_sum
        if trait_dist_sum:
            trait_normalizer = 1 / trait_dist_sum

        # We normalize both distributions

        probabilities[person]["gene"] = {
            gene_number: gene_number_prob * gene_normalizer
            for gene_number, gene_number_prob in probabilities[person]["gene"].items()
        }

        probabilities[person]["trait"] = {
            have_trait: have_trait_prob * trait_normalizer
            for have_trait, have_trait_prob in probabilities[person]["trait"].items()
        }


if __name__ == "__main__":
    main()
