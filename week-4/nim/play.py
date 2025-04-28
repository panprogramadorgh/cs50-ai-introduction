from nim import train, play

model = train(1_000)
play(model)

# GAMES = 1000
# """
# Number of games to be played for both ai models.
# """

# first, second = train(50), train(500)
# models = {first.model_name: 0, second.model_name: 0}

# print(f"Both models are competing each other {GAMES} times ...")

# for i in range(GAMES):
#     winner = ai_confrontation([first, second])
#     models[winner.model_name] += 1

# print("Printing scores for both trained models:")
# print(models)
