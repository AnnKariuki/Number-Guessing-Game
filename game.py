import random
import time
import math
def main():
    # \n means drop one line when outputting to terminal. print() function automatically adds a newline after each output plus our extra \n we get another drop hence the space break
    # The print() function has an optional keyword argument named end that lets us choose how we end each line. end="" overrides python default \n
    print("Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.\nGuess the correct number and win the game\n")
    rounds = 1
    # one source of truth for what difficultly levels exist. we don't want to have to change two dictionaries when we add a difficulty level eg expert level
    difficulties = {
        1: {"name": "Easy", "chances": 10},
        2: {"name": "Medium", "chances": 5},
        3: {"name": "Hard", "chances": 3}
    }
    high_scores = {key: math.inf for key in difficulties} # remember we don't have to do difficulties.keys() because iterating over a dictionary already iterates over its keys.
    # high_scores = {difficulties[key]: math.inf for key in difficulties.keys()} # TypeError: unhashable type: 'dict'. difficulties[key] evaluates to a dictionary and we cannot use a dictionary as a key inside the high_scores dictionary.
    # The TypeError: unhashable type: 'dict' occurs when you attempt to use a mutable dictionary as a dictionary key or add it to a set. In Python, sets and dictionary keys require hashable (immutable) objects—like strings, integers, or tuples—so that their values remain constant and can be quickly looked up
    # high_scores = {
    #     1: math.inf,
    #     2: math.inf,
    #     3: math.inf
    # }
    # we have 3 values that serve the same purpose so we replaced them with a dictionary that associates its difficulty with its high score
    # highest_score_easy = math.inf # float('inf')
    # highest_score_medium = math.inf 
    # highest_score_hard = math.inf 
    # i don't want to show the high score of a level the user did not play

    # while the game is running
    while True:
        # starting up the round. 
        print(f"Please select the difficulty level of round {rounds}:")
        for key, value in difficulties.items():
            print(f"{key}. {value['name']} ({value['chances']} chances)")

        difficulty_input = input("Enter your choice: ")
        if not difficulty_input.isdigit():
            raise ValueError("Difficulty must be an integer")
        difficulty = int(difficulty_input)
        # picked {} rather than set([1,2,3]) constructor since the constructor build up the set in o (n) time since we have to iterate over the list to populate set. in this case it doesn't really matter since there are 3 values o(3) = o(1)
        if difficulty not in difficulties: # we don't need to check  difficulties.keys() when checking whether a difficulty exists in a dictionary. Python checks dictionary keys by default.
            raise ValueError(f"Difficulty level must be one of {[*difficulties]}") # list(difficulties.keys())

        print()
        chances = difficulties[difficulty]['chances']
        print(f"Great! You have selected the {difficulties[difficulty]['name']} difficulty level. You have {chances} chances to guess the correct number.\n")
        # if difficulty == 1:
        #     print("Great! You have selected the Easy difficulty level. You have 10 chances to guess the correct number.\n")
        #     chances = 10
        # elif difficulty == 2:
        #     print("Great! You have selected the Medium difficulty level. You have 5 chances to guess the correct number.\n")
        #     chances = 5
        # elif difficulty == 3:
        #     print("Great! You have selected the Hard difficulty level. You have 3 chances to guess the correct number.\n")
        #     chances = 3

        print(f"Lets start the round {rounds}")
        # we need a number to be guessed for this round
        number_to_be_guessed = 1 #random.randint(2, 99) # inclusive of the boundary numbers and since we want between 1 and 100 we use 2 and 99 as the endpoints
        # keep track of the attempts in this round
        attempts = 0
        won = False
        start_time = time.time()
        while attempts < chances:
            # on attempt 1 user guesses
            user_input = input("Enter your guess: ")
            if not user_input.isdigit():
                raise ValueError("Guess must be an integer")
            user_guess = int(user_input)
            if user_guess < 1 or user_guess > 100:
                raise ValueError("Guess must be an integer between 1 and 100")
            # increment attempts after validating input
            attempts += 1
            if user_guess == number_to_be_guessed:
                end_time = time.time()
                print(f"Congratulations! You guessed the correct number in {attempts} attempts and it took you {end_time - start_time} seconds. Impressive!")
                won = True
                # with the dictionary we don't need these conditional. we are doing the same thing in each branch
                high_scores[difficulty] = min(high_scores[difficulty], attempts)
                # highest_score_easy = min(highest_score_easy, attempts)
                break
            # we don't need this check. it is redundant. if guess is correct we break out of the loop
            #if user_guess != number_to_be_guessed:
            elif number_to_be_guessed < user_guess:
                print(f"Incorrect! The number is less than {user_guess}")
            else:
                print(f"Incorrect! The number is greater than {user_guess}")
        # if we break out the loop without winning ie attempts is greater than chances
        if not won: # this is the same as if won == False or if won is False
            print(f"You ran out of chances")
        print()
        print("Would you like to play another round?\n")
        another_round = input("Yes or No: ")
        # if anything other than yes
        if another_round.lower() != "yes":
            # break out of the main for loop
            break
        print()
        rounds += 1
    print("\nIn summary\n")
    #  The second check is for the case that a user plays a round or many rounds and wins nothing, we should not print their high score cause they don't have one. without this we 
    # would have For Easy/Medium/Hard level your highest score was inf
    # if played_in_easy_mode and highest_score_easy < math.inf: we don't need the first condition cause if the highest score for the level moved downwards it means the level was played
    for key, value in high_scores.items():
        if value < math.inf:
            print(f"Your best performance on {difficulties[key]['name']} difficulty was guessing the number in {value} attempts")
    # if high_scores[1] < math.inf: 
    #     print(f"For Easy level your highest score (fewest number of attempts it took to guess the number) was {high_scores[1]}")
    # if high_scores[2] < math.inf:
    #     print(f"For Medium level your highest score (fewest number of attempts it took to guess the number) was {high_scores[2]}")
    # if high_scores[3] < math.inf:
    #     print(f"For Hard level your highest score (fewest number of attempts it took to guess the number) was {high_scores[3]}")
    print("\nThank you for playing. Goodbye")

if __name__ == "__main__":
    main()


# Question; do we want each round to have it's own difficulty or they pick the difficulty once and that is the difficulty for all rounds
# the additional requirements says "Keep track of the user's high score (i.e., the fewest number of attempts it took to guess the number under a specific difficulty level)."
# I think this means every round different difficulty level