import pycountry
from os import system
import msvcrt

players = ["Alex", "Patric"]


def main(players, max_rounds = 1):
    countries = {c.name: c for c in pycountry.countries}
    score = {p: {} for p in players}
    guessed_countries = {}
    exit_word = "123"

    round = 1

    print("Welcome to our Geography Quiz!")
    print(f"To give up, please type in '{exit_word}' as a guess at any time.")
    input(f"Press ENTER to start!!")

    while round <= max_rounds:
        system("cls")
        print(f"Round {round}!")
        for p in players:
            while True:
                is_hit = False
                guess = input(f"Please enter your guess, {p}:\n")
                
                if guess == exit_word:
                    print(f"{p} has given up. This is the last round.")
                    max_rounds = 0
                    break

                if countries.get(guess):
                    hit = guess
                else:
                    try:
                        all_hits = [hit.name for hit in pycountry.countries.search_fuzzy(guess)]
                        hits = [hit for hit in all_hits if not guessed_countries.get(hit)]
                    except Exception:
                        hits = []

                    if len(hits) > 1:
                        print("Your guess generated more than one result. Please be more specific.")
                        continue
                    if not len(hits):
                        print(f"There is no country called {guess}. Please try again.")
                        continue
                    
                    hit = hits[0]

                prev_guess = guessed_countries.get(hit)
                if prev_guess:
                    print(f"{hit} has already been guessed by {prev_guess}. Please try again.")
                elif countries.get(hit):
                    guessed_countries[hit] = countries.pop(hit)
                    print(f"{hit} is a country! Good Job, {p}!")
                    score[p][hit] = None
                    guessed_countries.update({hit:p})
                    break
                else:
                    print(f"There is no country called {guess}. Please try again.")

        print(f"Score after round {round}:")
        for player, guesses in score.items():
            print(f"{player}: {len(guesses)}")

        if round < max_rounds:
            input("Press ENTER to the next round")

        round += 1

    max_score = 0
    for p, s in score.items():
        if len(s) > max_score:
            max_score = len(s)
            winner = p
    
    print(f"The winner is {winner}!")
    return score


if __name__ == "__main__":
    score = main(players, max_rounds=300)
