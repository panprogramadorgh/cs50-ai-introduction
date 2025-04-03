
from typing import Iterable

# Dictionary utilities

def has_key(key: str, dictionary: dict):
  """Returns True whether contains `key`"""
  return key in dictionary.keys()

# Other utils

def quick_sort(iter: list[int], left: int = None, right: int = None):
  if None in (left, right):
    return quick_sort(iter, 0, len(iter) - 1)
  # TODO: Terminar quick sort    

def main():
  print(hash("hola"))

if __name__ == "__main__":
  main()