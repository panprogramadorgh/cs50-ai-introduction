import numpy as np
from nim import train, play, ai_confrontation

GAMES = 10

print("Training first AI")
first_agent = train(500)

print("Training seconnd AI")
second_agent = train(5000)


for i in range(GAMES):
    print(f"Game - {i}")
    ai_confrontation(np.array([first_agent, second_agent]))
