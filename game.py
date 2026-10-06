import random
import time
import math
from typing import TypedDict
# decided to leave difficulties and max retries here since they are configuration and they don't change as the game runs
# I will move high scores down to main because it is mutable and is game state and changes as the player plays
Difficulty = TypedDict("Difficulty", {"name": str, "chances": int})
DIFFICULTIES: dict[int, Difficulty] = {
    1: {"name": "Easy", "chances": 10},
    2: {"name": "Medium", "chances": 5},
    3: {"name": "Hard", "chances": 3}
}
MAX_RETRIES = 3

def display_welcome_message() -> None:
    print("Welcome to the Number Guessing Game!\n"
    "I'm thinking of a number between 1 and 100.\n"
    "Guess the correct number and win the game\n")

def select_difficulty(rounds: int) -> int:
    print(f"Please select the difficulty level of round {rounds}:")
    for key, value in DIFFICULTIES.items():
        print(f"{key}. {value['name']} ({value['chances']} chances)")
    retries = 0
    while retries < MAX_RETRIES:
        difficulty_input = input("Enter your choice: ")
        if difficulty_input.isdigit() and int(difficulty_input) in DIFFICULTIES:
            return int(difficulty_input)
        print(f"Invalid Input. Difficulty Level must be an integer and/or must be one of {[*DIFFICULTIES]}.\n")
        retries += 1
    raise ValueError(f"Exceeded maximum attempts ({MAX_RETRIES}) to input a valid difficulty level. Exiting program.")

def get_user_guess() -> int:
    retries = 0
    while retries < MAX_RETRIES:
        user_input = input("Enter your guess: ")
        if user_input.isdigit() and int(user_input) >= 1 and int(user_input) <= 100:
            return int(user_input)
        print("Guess must be an integer and must be between 1 and 100\n")
        retries += 1
    raise ValueError(f"Exceeded maximum attempts ({MAX_RETRIES}) to input a valid guess. Exiting program.")

def get_hint(chances: int, number_to_be_guessed: int, user_guess: int) -> int:
    hint_ask = input("Would you like a hint? Caution: Accepting a hint costs one chance. Yes or No:")
    if not hint_ask.strip().lower().startswith('y'):
        return chances
    hint_dict = {
        1: "range_hint",
        2: "parity_hint",
        3: "divisibility_hint",
        4: "distance_hint",
        5: "digit_hint",
        6: "comparison_hint"
    }
    type_of_hint = hint_dict[random.randint(1,6)] 
    if type_of_hint == "range_hint":
        lower_bound = (number_to_be_guessed // 10) * 10
        higher_bound = lower_bound + 10
        if number_to_be_guessed == 100:
            lower_bound = (number_to_be_guessed - 1) // 10 * 10
            higher_bound = lower_bound + 10
        print(f"The number is between {lower_bound} and {higher_bound}")
    elif type_of_hint == "parity_hint":
        if number_to_be_guessed % 2 == 0:
            print(f"The number is even")
        elif number_to_be_guessed % 2 == 1:
            print(f"The number is odd")
    elif type_of_hint == "divisibility_hint":
        if number_to_be_guessed % 11 == 0:
            print("Number is divisible by 11")
        elif number_to_be_guessed % 7 == 0:
            print("Number is divisible by 7")
        elif number_to_be_guessed % 5 == 0:
            print("Number is divisible by 5")
        elif number_to_be_guessed % 3 == 0:
            print("Number is divisible by 3")
        elif number_to_be_guessed % 2 == 0:
            print("Number is divisible by 2")
        else:
            print("Number is not divisible by 2, 3, 5, 7, or 11")
    elif type_of_hint == "distance_hint":
        distance = number_to_be_guessed - user_guess
        print(f"You are within {abs(distance)} of the correct value")
    elif type_of_hint == "digit_hint":
        if 1 <= number_to_be_guessed <= 9:
            print("The number has 1 digit")
        elif 10 <= number_to_be_guessed <= 99:
            print("The number has 2 digits")
        elif number_to_be_guessed == 100:
            print("The number has 3 digits")
    elif type_of_hint == "comparison_hint":
        if number_to_be_guessed < user_guess:
            print(f"The number is less than {user_guess}")
        else:
            print(f"The number is greater than {user_guess}")
    chances -= 1 # can not change this value in another function. scope
    return chances

def play_round(difficulty: int, rounds: int) -> int| None:
    # doesn't know about high score. only job is to play game. updating is done in main. separation of responsibilities
    chances = DIFFICULTIES[difficulty]['chances']
    difficulty_name = DIFFICULTIES[difficulty]['name']
    print(f"\nGreat! You have selected the {difficulty_name} difficulty level. You have {chances} chances to guess the correct number.\n")
    print(f"Let's start round {rounds}")
    number_to_be_guessed = random.randint(1, 100)
    attempts = 0
    start_time = time.perf_counter()
    while attempts < chances:
        user_guess = get_user_guess()
        attempts += 1
        if user_guess == number_to_be_guessed:
            end_time = time.perf_counter()
            print(f"Congratulations! You guessed the correct number in {attempts} attempts and it took you {end_time - start_time} seconds. Impressive!")
            return attempts
        if attempts + 1 < chances:
            chances = get_hint(chances, number_to_be_guessed, user_guess)
    print("You ran out of chances")
    return None

def wants_another_round() -> bool:
    print("\nWould you like to play another round?\n")
    another_round = input("Yes or No: ")
    return another_round.strip().lower().startswith("y")

def display_summary(rounds: int, high_scores: dict[int, float|int] ) -> None:
    print("\nIn summary\n")
    print(f"You played a total of {rounds} rounds")
    won_a_game = False
    for key, value in high_scores.items():
        if value < math.inf:
            print(f"Your best performance on {DIFFICULTIES[key]['name']} difficulty was guessing the number in {value} attempts")
            won_a_game = True
    if not won_a_game:
        print("No high scores were recorded")
    print("\nThank you for playing. Goodbye")

def main() -> None:
    rounds = 1
    high_scores: dict[int, float | int] = {key: math.inf for key in DIFFICULTIES} 
    display_welcome_message()
    while True:
        difficulty = select_difficulty(rounds)
        attempts = play_round(difficulty, rounds)

        if attempts is not None:
            high_scores[difficulty] = min(high_scores[difficulty], attempts)
            
        if not wants_another_round():
            break
        print()
        rounds += 1
    display_summary(rounds, high_scores)

if __name__ == "__main__":
    main()