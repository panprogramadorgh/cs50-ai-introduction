# Each person should belong to a house
# Each house should include just one person

from logic import *

houses = ["Diaz", "Gomez", "Sanchez"]
people = ["Alberto", "Perro", "Juan"]
symbols = []
knowledge = And()

for house in houses:
    bindings = []
    for person in people:
        s = Symbol(f"{person}{house}")
        bindings.append(s)
        symbols.append(s)
    knowledge.add(Or(*bindings))

for person in people:
    for this_house in houses:
        for other_house in houses:
            if this_house != other_house:
                knowledge.add(
                    Implication(
                        Symbol(f"{person}{this_house}"),
                        Not(Symbol(f"{person}{other_house}")),
                    )
                )

for house in houses:
    for this_person in people:
        for other_person in people:
            if this_house != other_house:
                knowledge.add(Implication(Symbol(f"{this_person}{house}"), Not(Symbol(f"{other_person}{house}"))))

knowledge.add(Or(Symbol("AlbertoDiaz"), Symbol("AlbertoGomez")))
knowledge.add(Not(Symbol(f"PerroGomez")))
knowledge.add(Symbol("JuanDiaz"))

for s in symbols:
    if model_check(knowledge, s):
        print(f"{s}: YES")
    elif not model_check(knowledge, Not(s)):
        print(f"{s}: MAYBE")
