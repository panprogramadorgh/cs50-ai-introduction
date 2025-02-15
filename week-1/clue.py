from logic import *

# Personas implicadas
mustard = Symbol("mustard")
plum = Symbol("plum")
scarlet = Symbol("scarlet")
characters = [mustard, plum, scarlet]

# Lugares implicados
ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
places = [ballroom, kitchen, library]

# Armas implicadas
knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]

# Todos los simbolos disponibles
symbols = characters + places + weapons

# Verifica el entailment para todos los simbolos disponibles dado el conocimiento propocionado
def check_knowledge(knowledge: Sentence):
  for symbol in symbols:
    if model_check(knowledge, symbol):
      print(f"{symbol}: YES")
    elif not model_check(knowledge, Not(symbol)):
      print(f"{symbol}: MAYBE")

knowledge = And(
  Or(*characters),
  Or(*places),
  Or(*weapons)
)

knowledge.add(And(
  Or(
  revolver, knife
  ),
  Not(wrench)
))

knowledge.add(Not(mustard))
knowledge.add(Not(knife))

knowledge.add(Or(
  Not(scarlet), Not(ballroom)
))

knowledge.add(Not(ballroom))
knowledge.add(Not(kitchen))
knowledge.add(Not(plum))


check_knowledge(knowledge)