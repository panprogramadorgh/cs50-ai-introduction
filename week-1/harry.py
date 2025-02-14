from logic import *

def main():
  rain = Symbol("rain") # It is raining
  hugrid = Symbol("hugrid") # Harry visited Hugrid
  dumbledore = Symbol("dumbledore") # Harry visited Dumbledore

  knowledge = And(
    Implication(hugrid, Not(rain)),
    Or(hugrid, dumbledore),
    Not(And(hugrid, dumbledore)),

    rain
  )

  result = model_check(knowledge, dumbledore)
  print(result)


if __name__ == "__main__":
  main()
