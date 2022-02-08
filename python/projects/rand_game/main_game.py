# """
# my gambling game consist of 3 rounds, on each round the player will play against
# the computer, each will be given a chance to win by running a random number
# 1 - 3 , the game will declare the winner of each round and the total game score
# """
import random

try:
    player1_total_score = 0
    player2_total_score = 0

    for x in range(3):
        round_start_message = "Round {} is beginning"
        print(round_start_message.format(x + 1))

        player1_round_score = random.randrange(1, 4, 1)
        player2_round_score = random.randrange(1, 4, 1)

        round_win_message = "Player score is: {}, Computer score is: {}"
        print(round_win_message.format(player1_round_score, player2_round_score))

        winner_message = "{} won round number {}"
        if player1_round_score > player2_round_score:
            print(winner_message.format("Player", x))
            player1_total_score = player1_total_score + player1_round_score
        elif player1_round_score < player2_round_score:
            print(winner_message.format("Computer", x))
            player2_total_score = player2_total_score + player1_round_score
        else:
            print(winner_message.format("No one!", x))

    if player1_total_score > player2_total_score:
        print("player 1 won the games !!!")
    elif player2_total_score > player1_total_score:
        print("player 2 won the games !!!")
    else:
        print("It's a TIE !!!")
except:
    print("An exception occurred")
