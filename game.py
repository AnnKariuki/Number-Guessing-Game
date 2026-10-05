import random
import time
import math
def main():
    print("Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.\nGuess the correct number and win the game\n")
    rounds = 1
    difficulties = {
        1: {"name": "Easy", "chances": 10},
        2: {"name": "Medium", "chances": 5},
        3: {"name": "Hard", "chances": 3}
    }
    high_scores = {key: math.inf for key in difficulties} 
    while True:
        print(f"Please select the difficulty level of round {rounds}:")
        for key, value in difficulties.items():
            print(f"{key}. {value['name']} ({value['chances']} chances)")
        retries = 0
        max_retries = 3
        while retries < max_retries:
            difficulty_input = input("Enter your choice: ")
            if difficulty_input.isdigit() and int(difficulty_input) in difficulties:
                break
            print(f"Invalid Input. Difficulty Level must be an integer and/or must be one of {[*difficulties]}.\n")
            retries += 1
        else:
            raise ValueError(f"Exceeded maximum attempts ({max_retries}) to input a valid difficulty level. Exiting program.")
        
        difficulty = int(difficulty_input)
        print()
        chances = difficulties[difficulty]['chances']
        print(f"Great! You have selected the {difficulties[difficulty]['name']} difficulty level. You have {chances} chances to guess the correct number.\n")

        print(f"Let's start the round {rounds}")
        number_to_be_guessed = 1 # random.randint(1, 100)
        attempts = 0
        start_time = time.perf_counter()
        while attempts < chances:
            retries = 0
            max_retries = 3
            while retries < max_retries:
                user_input = input("Enter your guess: ")
                if user_input.isdigit() and int(user_input) >= 1 and int(user_input) <= 100:
                    break
                print("Guess must be an integer and must be between 1 and 100\n")
                retries += 1
            else:
                raise ValueError(f"Exceeded maximum attempts ({max_retries}) to input a valid guess. Exiting program.")
            user_guess = int(user_input)
            attempts += 1
            if user_guess == number_to_be_guessed:
                end_time = time.perf_counter()
                print(f"Congratulations! You guessed the correct number in {attempts} attempts and it took you {end_time - start_time} seconds. Impressive!")
                high_scores[difficulty] = min(high_scores[difficulty], attempts)
                break
            elif number_to_be_guessed < user_guess:
                print(f"Incorrect! The number is less than {user_guess}")
            else:
                print(f"Incorrect! The number is greater than {user_guess}")
        else:
            print(f"You ran out of chances")
        print()
        print("Would you like to play another round?\n")
        another_round = input("Yes or No: ")
        if not another_round.strip().lower().startswith('y'):
            break
        print()
        rounds += 1
    print("\nIn summary\n")
    print(f"You played a total of {rounds} rounds")
    won_a_game = False
    for key, value in high_scores.items():
        if value < math.inf:
            print(f"Your best performance on {difficulties[key]['name']} difficulty was guessing the number in {value} attempts")
            won_a_game = True
    if not won_a_game:
        print("No high scores were recorded")
    print("\nThank you for playing. Goodbye")

if __name__ == "__main__":
    main()