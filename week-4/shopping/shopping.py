import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


# Not provided implementations

# Literal strings of the months of the year
months = (
    "Jun",  # 0
    "Feb",
    "Mar",
    "Apr",
    "May",
    "June",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",  # 11
)


def month_parser(month: str):
    if month not in months:
        raise ValueError(f"Invalid month was provided: '{month}'")
    return months.index(month)


def bool_lit_parser(lit: str):
    """
    Not case sensitive boolean literal parser.

    Examples:
        - "TRUE" -> True
        - "backed_beans" -> False"""
    return int(lit.lower() == "true")


def visitortp_lit_parser(lit: str):
    return int(lit.lower() == "returning_visitor")


def parse_row(row: list[str]):
    """
    In charge of field type convertions for each row.

    Parameters:
        - row — The current CSV row including the final `revenue` column.
    """

    # The whole parsed row will be stored here
    parsed = []

    parsers = (
        int,  # Administrative
        float,  # ADministrative_Duration
        int,  # Informational
        float,  # Informational_Duration
        int,  # ProductRelated
        float,  # ProductRelated_Duration
        float,  # BounceRates
        float,  # ExitRates
        float,  # PageValues
        float,  # SpecialDay
        month_parser,  # Month
        int,  # OperatingSystems
        int,  # Browser
        int,  # Region
        int,  # TrafficType
        visitortp_lit_parser,  # VisitorType
        bool_lit_parser,  # Weekend
        bool_lit_parser,  # Revenue
    )

    parsers_len = len(parsers)
    if parsers_len != len(row):
        raise ValueError(f"Invalid row size. Expected size: {parsers_len}")

    for field, parser in zip(row, parsers):
        parsed.append(parser(field))

    return parsed


# ---------

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename: str):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    labels: list[int] = []
    evidence: list[list[int | float]] = []

    with open(filename, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i < 1:
                continue
            prow = parse_row(row)
            evidence.append(prow[0 : len(prow) - 1])
            labels.append(prow[len(prow) - 1])

    return (evidence, labels)


def train_model(evidence: list[list], labels: list[int]):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    """ 
    Initialized model with scikitlearn and fit them.
    
    Resources:
        - https://scikit-learn.org/stable/auto_examples/neighbors/plot_classification.html#sphx-glr-auto-examples-neighbors-plot-classification-py
        
        - https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation
    """

    model = KNeighborsClassifier(n_neighbors=1)

    raise NotImplementedError


def evaluate(labels: list[int], predictions: list[int]):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
