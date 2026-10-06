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

def play_round(difficulty: int, rounds: int) -> int| None:
    # doesn't know about high score. only job is to play game. updating is done in main. separation of responsibilities
    chances: int = DIFFICULTIES[difficulty]['chances']
    difficulty_name = DIFFICULTIES[difficulty]['name']
    print(f"\nGreat! You have selected the {difficulty_name} difficulty level. You have {chances} chances to guess the correct number.\n")
    print(f"Let's start round {rounds}")
    number_to_be_guessed = 1 # random.randint(1, 100)
    attempts = 0
    start_time = time.perf_counter()
    while attempts < chances:
        user_guess = get_user_guess()
        attempts += 1
        if user_guess == number_to_be_guessed:
            end_time = time.perf_counter()
            print(f"Congratulations! You guessed the correct number in {attempts} attempts and it took you {end_time - start_time} seconds. Impressive!")
            return attempts
        elif number_to_be_guessed < user_guess:
            print(f"Incorrect! The number is less than {user_guess}")
        else:
            print(f"Incorrect! The number is greater than {user_guess}")
    print(f"You ran out of chances")
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