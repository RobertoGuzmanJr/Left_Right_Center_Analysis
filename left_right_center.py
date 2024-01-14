import numpy as np
import random
import statistics as stats

AVERAGE_NUMBER_OF_TURNS = {}
STANDARD_DEVIATION_NUMBER_OF_TURNS = {}
AVERAGE_WIN_PERCENTAGE = {}
AVERAGE_DEVIATION_FROM_FAIRNESS_PERCENTAGE = {}
NUMBER_OF_GAMES = 1000000
MAX_NUM_PLAYERS = 21
SIG_FIG_ROUNDING = 6


def play_game(num_players):
    player_balances = [3]*num_players
    current_player = 0
    center_balance = 0
    num_turns = 0
    while check_game_over(player_balances) < 0:
        num_dice_to_roll = min(3, player_balances[current_player])
        dice_results = roll_dice(num_dice_to_roll)
        for die_result in dice_results:
            if die_result == "Center":
                player_balances[current_player] -= 1
                center_balance += 1
            elif die_result == "Left":
                player_balances[current_player] -= 1
                player_balances[current_player-1] += 1
            elif die_result == "Right":
                player_balances[current_player] -= 1
                player_balances[(current_player + 1) % num_players] += 1
        num_turns += 1
        current_player = (current_player + 1) % num_players
    return player_balances, num_turns


def check_game_over(player_balances):
    player_with_money = None
    for i in range(0, len(player_balances)):
        if player_balances[i] > 0 and player_with_money is not None:
            return -1
        elif player_balances[i] > 0:
            player_with_money = i
    return i


def roll_dice(num_dice):
    result = []
    for i in range(num_dice):
        number = random.randint(0,5)
        if number == 5:
            result.append("Center")
        elif number == 4:
            result.append("Right")
        elif number == 3:
            result.append("Left")
        else:
            result.append("Keep")
    return result


def determine_winning_player(player_balances):
    return player_balances.index(max(player_balances))


def calculate_final_win_distribution(all_wins):
    num_wins_by_player = {}
    for win in all_wins:
        if win in num_wins_by_player:
            num_wins_by_player[win] += 1
        else:
            num_wins_by_player[win] = 1
    final_wins = [0]*len(num_wins_by_player.keys())
    for i in range(len(final_wins)):
        final_wins[i] = num_wins_by_player[i]
    return final_wins


def run_simulation():
    current_num_players = 2
    while current_num_players < MAX_NUM_PLAYERS:
        expected_fair_results = [1/current_num_players]*current_num_players
        current_best_player_results = []
        current_num_turns = []
        for current_game_number in range(NUMBER_OF_GAMES):
            game_result = play_game(current_num_players)
            final_player_balances = game_result[0]
            num_turns = game_result[1]
            winning_player = determine_winning_player(final_player_balances)
            current_best_player_results.append(winning_player)
            current_num_turns.append(num_turns)
        final_win_distribution = calculate_final_win_distribution(current_best_player_results)
        final_win_percents = [x/NUMBER_OF_GAMES for x in final_win_distribution]

        # collect statistics on the winnings per player.
        AVERAGE_WIN_PERCENTAGE[current_num_players] = final_win_percents
        AVERAGE_DEVIATION_FROM_FAIRNESS_PERCENTAGE[current_num_players] = list(np.subtract(
            final_win_percents, expected_fair_results))

        # collect statistics on the number of turns.
        AVERAGE_NUMBER_OF_TURNS[current_num_players] = stats.mean(current_num_turns)
        STANDARD_DEVIATION_NUMBER_OF_TURNS[current_num_players] = stats.stdev(current_num_turns)

        current_num_players += 1


def present_results():
    print("Now presenting results")
    print(f"Num Games = {NUMBER_OF_GAMES}")
    current_num_players = 2
    while current_num_players < MAX_NUM_PLAYERS:
        print("--------------------------------------")
        print(f"Num Players = {current_num_players}")
        print(f"Mean Num Turns = {round(AVERAGE_NUMBER_OF_TURNS[current_num_players], SIG_FIG_ROUNDING)}")
        print(f"Std Dev Num Turns = {round(STANDARD_DEVIATION_NUMBER_OF_TURNS[current_num_players], SIG_FIG_ROUNDING)}")
        print(f"Player Win Probs = {[round(x, SIG_FIG_ROUNDING) for x in AVERAGE_WIN_PERCENTAGE[current_num_players]]}")
        print(f"Player Dev From Fairness = {[round(x, SIG_FIG_ROUNDING) for x in AVERAGE_DEVIATION_FROM_FAIRNESS_PERCENTAGE[current_num_players]]}")
        best_player = determine_winning_player(AVERAGE_WIN_PERCENTAGE[current_num_players])
        print(f"The best position is {best_player} with average win prob = {round(AVERAGE_WIN_PERCENTAGE[current_num_players][best_player], SIG_FIG_ROUNDING)} which deviates from fairness by = {round(AVERAGE_DEVIATION_FROM_FAIRNESS_PERCENTAGE[current_num_players][best_player], SIG_FIG_ROUNDING)}")
        current_num_players += 1


if __name__ == "__main__":
    run_simulation()
    present_results()
