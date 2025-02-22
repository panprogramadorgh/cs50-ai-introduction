from sys import exit
from typing import Iterable
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

def upwards_round(n: float):
    return int(n) + 1

def Xor(*conjuncts: Iterable[Sentence]):
    and_conjunction = And(Or(*conjuncts))
    for cy in conjuncts[: upwards_round(len(conjuncts) / 2)]:
        for cx in conjuncts[int(len(conjuncts) / 2):]:
            if cy == cx:
                continue
            and_conjunction.add(Not(And(cy, cx)))
    return and_conjunction


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Xor(AKnight, AKnave),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),

    Implication(AKnight, And(AKnave, BKnave)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),
    
    Implication(AKnight, BKnight),
    Implication(BKnight, AKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Xor(AKnight, AKnave),
    Xor(BKnight, BKnave),
    Xor(CKnight, CKnave),
    
    Implication(BKnight, And(Implication(AKnight, AKnave), CKnave)),
    Implication(CKnight, AKnight) 
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol} -- Entails")
                elif model_check(knowledge, Not(symbol)): 
                    print(f"    {symbol} -- Not entails")
                else:
                    print(f"    {symbol} -- Maybe entails")


if __name__ == "__main__":
    main()
