import pickle

from fourInRowGame import FourInRowGame, Chip

with open("actorCriticLvl5Yellow.pkl", "rb") as f:
    agent_yellow = pickle.load(f)

with open("actorCriticLvl6Red.pkl", "rb") as f:
    agent_red = pickle.load(f)

def game(yellow_player, red_player, env):

    gameover = False
    max_games = int((env.rows * env.columns)/2)
    i = 0
    last_move = "YELLOW"

    while((not gameover) and (i < max_games)):
        last_move = "YELLOW"
        col = yellow_player.select_col(env)
        gameover = env.play_game(Chip.YELLOW,col)
        if not gameover:
            last_move = "RED"
            col = red_player.select_col(env)
            gameover = env.play_game(Chip.RED,col)
        i = i + 1

    return last_move

env = FourInRowGame(6, 7)

tracker = {
    "RED":0,
    "YELLOW":0
}

for i in range(0,1000):
    if i % 100 == 0:
        print(f"Game {i}")
        env.print()
    env.reset()
    winner = game(agent_yellow, agent_red, env)
    tracker[winner] = tracker[winner] + 1

print(tracker)
env.print()


