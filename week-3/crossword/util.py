from typing import Iterable

# Dictionary utilities


def has_key(key: str, dictionary: dict):
    """Returns True whether contains `key`"""
    return key in dictionary.keys()


# Algorithms


def quick_sort(iter: list[int], left: int = 0, right: int = None):
    """
    ### QuickSort algorithm

    - Declare a `i` variable which will be the next pivot pos and will have an initial value of 0

    - Iterates for each `iter` value

    - For each iteration, if `value` is less than the current pivot value, then swap the value at next pivot pos by the iteration `value`
    """

    if right is None:
        right = len(iter) - 1

    if left >= right:
        return iter

    pivot = iter[right]  # Current pivot value
    i = left  # Next pivot index

    for j in range(left, right):
        if iter[j] <= pivot:
            iter[i], iter[j] = iter[j], iter[i]
            i += 1

    iter[i], iter[right] = iter[right], iter[i]

    quick_sort(iter, left, i - 1)
    quick_sort(iter, i + 1, right)

    return iter


def main():
    pass


if __name__ == "__main__":
    main()
