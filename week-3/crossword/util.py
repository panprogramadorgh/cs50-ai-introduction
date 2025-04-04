from typing import Iterable, Any
import sys

# Dictionary utilities


def has_key(key: str, dictionary: dict):
    """Returns True whether contains `key`"""
    return key in dictionary.keys()


# Algorithms

DESC_SORT, ASC_SORT = 0, 1

def quick_sort(
    iter: list[Any],
    left: int = 0,
    right: int = None,
    dir: int= ASC_SORT, # DESC_SORT | ASC_SORT
    get_value=lambda x: x
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

    pivot = get_value(iter[right])  # Current pivot value
    i = left  # Next pivot index

    for j in range(left, right):
        if compare(get_value(iter[j]), pivot):
            iter[i], iter[j] = iter[j], iter[i]
            i += 1

    iter[i], iter[right] = iter[right], iter[i]

    quick_sort(iter, left=left, right=i - 1, get_value=get_value, dir=dir)
    quick_sort(iter, left=i + 1, right=right, get_value=get_value, dir=dir)

    return iter


def main():

    domains_len = {
        "first": 22, 
        "second": 44,
        "third": 77
    }

    sorted_domains = [pair[1] for pair in quick_sort(list(domains_len.items()), get_value=(lambda pair: pair[1]), dir=ASC_SORT)]

    print(sorted_domains)


if __name__ == "__main__":
    main()
