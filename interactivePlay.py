import pickle

from fourInRowGame import FourInRowGame, Chip

with open("actorCriticLvl5Yellow.pklx", "rb") as f:
    agent_yellow = pickle.load(f)

def validateInput(input):
    if input not in ["1","2","3","4","5","6","7"]:
        return False
    return True

def game(yellow_player, env):

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

            print("\r\n1 2 3 4 5 6 7")
            print("_____________")
            env.print()
            print("\r\nSelect column")
            print(">", end="")
            playerCol = input()
            while not validateInput(playerCol):
                print("Invalid column")
                playerCol = input()

            gameover = env.play_game(Chip.RED, int(playerCol)-1)
            
        i = i + 1

    return last_move

env = FourInRowGame(6, 7)

winner = game(agent_yellow, env)
print("\r\n" + winner + " WON!!!")
env.print()
