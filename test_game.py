import unittest
from unittest.mock import patch, call
import game
import math
class TestGame(unittest.TestCase):
    def setUp(self):
        # I am patching print before each test because I am tired of all the printed statements in the output in the terminal when i run my tests
        # tests like test_display_welcome_message can still inspect the mock so that is fine and terminal stays clean
        self.print_patcher = patch('game.print')
        self.mocked_print = self.print_patcher.start()
        self.addCleanup(self.print_patcher.stop)

    def test_display_welcome_message_prints_expected_message(self):
        game.display_welcome_message()
        self.mocked_print.assert_called_with("Welcome to the Number Guessing Game!\n"
        "I'm thinking of a number between 1 and 100.\n"
        "Guess the correct number and win the game\n")

    @patch('game.input')
    def test_select_difficulty_returns_valid_selection_when_given_valid_user_input(self, mocked_input):
        mocked_input.return_value = '2'
        result = game.select_difficulty(1)
        self.assertEqual(result, 2)

    @patch('game.input')
    def test_select_difficulty_raises_after_max_invalid_attempts(self, mocked_input):
        mocked_input.return_value = 'r'
        with self.assertRaises(ValueError):
            game.select_difficulty(1)
        self.assertEqual(mocked_input.call_count, 3)

        mocked_input.assert_has_calls([
            call("Enter your choice: "),
            call("Enter your choice: "),
            call("Enter your choice: "),
        ])

    @patch('game.input')
    def test_select_difficulty_returns_valid_selection_after_invalid_attempts(self, mocked_input):
        mocked_input.side_effect = ['r', '4', '2']

        result = game.select_difficulty(1)

        self.assertEqual(result, 2)
        self.assertEqual(mocked_input.call_count, 3)

        mocked_input.assert_has_calls([
            call("Enter your choice: "),
            call("Enter your choice: "),
            call("Enter your choice: "),
        ])

    @patch('game.input')
    def test_get_user_guess_returns_valid_guess(self, mocked_input):
        mocked_input.return_value = '2'
        result = game.get_user_guess()
        self.assertEqual(result, 2)

    @patch('game.input')
    def test_get_user_guess_raises_after_max_invalid_attempts(self, mocked_input):
        mocked_input.return_value = 'r'
        with self.assertRaises(ValueError):
            game.get_user_guess()
        self.assertEqual(mocked_input.call_count, 3)

        mocked_input.assert_has_calls([
            call("Enter your guess: "),
            call("Enter your guess: "),
            call("Enter your guess: "),
        ])

    @patch('game.input')
    def test_get_user_guess_returns_valid_guess_after_invalid_attempts(self, mocked_input):
        # side effect is useful when you need a sequence of deifferent args otherwise just use return_value
        mocked_input.side_effect = ['r', '101', '2']

        result = game.get_user_guess()

        self.assertEqual(result, 2)
        self.assertEqual(mocked_input.call_count, 3)

        mocked_input.assert_has_calls([
            call("Enter your guess: "),
            call("Enter your guess: "),
            call("Enter your guess: "),
        ])

    @patch('game.input')
    def test_wants_another_round_returns_true_for_yes(self, mocked_input):
        mocked_input.return_value = "Yes"
        result = game.wants_another_round()
        self.assertTrue(result)

    @patch('game.input')
    def test_wants_another_round_returns_false_for_no(self, mocked_input):
        mocked_input.return_value = "No"
        result = game.wants_another_round()
        self.assertFalse(result)

    def test_display_summary_prints_high_scores_for_all_difficulties(self):
        high_scores = {
            1: 1,
            2: 2,
            3: 3
        }
        game.display_summary(3, high_scores)
        # assert_Called_with checks that the mocked object was last called with a certain agrument(most recent call) so this below will fail
        # self.mocked_print.assert_called_with("Your best performance on Easy difficulty was guessing the number in 1 attempts")
        # self.mocked_print.assert_called_with("Your best performance on Medium difficulty was guessing the number in 2 attempts")
        # self.mocked_print.assert_called_with("Your best performance on Hard difficulty was guessing the number in 3 attempts")
        
        # any_order=False means those calls must appear in that order. They can still have other calls before or after that sequence
        self.mocked_print.assert_has_calls(
             [
                 call("Your best performance on Easy difficulty was guessing the number in 1 attempts"),
                 call("Your best performance on Medium difficulty was guessing the number in 2 attempts"),
                 call("Your best performance on Hard difficulty was guessing the number in 3 attempts")
             ], any_order=False
        )
    def test_display_summary_prints_no_high_scores_when_no_games_won(self):
        high_scores = {
            1: math.inf,
            2: math.inf,
            3: math.inf
        }
        game.display_summary(3, high_scores)
        # this is wrong most recent call was print("\nThank you for playing. Goodbye") so assert_Called_with fails
        # self.mocked_print.assert_called_with("No high scores were recorded")

        # this is correct
        self.mocked_print.assert_has_calls(
            [
                call("No high scores were recorded")
            ]
        )

        # this is also correct 
        self.mocked_print.assert_any_call("No high scores were recorded")

    @patch('game.input') 
    def test_get_hint_returns_same_chances_when_hint_declined(self, mocked_input):
        mocked_input.return_value = "No"
        chances = 3
        self.assertEqual(3, game.get_hint(chances, 1, 5))

    # not testing all hints
    @patch('game.input') 
    @patch("game.random.randint")
    def test_get_hint_range_hint_prints_range_and_reduces_chances(self, random_hint_mocked, mocked_input):
        mocked_input.return_value = "Yes"
        random_hint_mocked.return_value = 1
        result = game.get_hint(3, 100, 5)
        self.mocked_print.assert_called_with("The number is between 90 and 100")
        self.assertEqual(result, 2)

    @patch("game.get_hint")
    @patch("game.time.perf_counter")
    @patch('game.get_user_guess') 
    @patch("game.random.randint")
    def test_play_round_returns_one_attempt_for_correct_first_guess_and_does_not_call_get_hint(self,mocked_no_to_be_guessed, mocked_user_guess, mock_counter, mocked_get_hint):
        # we will mock the start time and end_time using side effect where we can provide start and end time values for consecutive calls
        mock_counter.side_effect = [10.0, 12.5]
        mocked_no_to_be_guessed.return_value = 1
        mocked_user_guess.return_value = 1
        attempts = game.play_round(1,1)
        self.assertEqual(attempts, 1)
        self.mocked_print.assert_any_call("Congratulations! You guessed the correct number in 1 attempts and it took you 2.5 seconds. Impressive!")
        mocked_get_hint.assert_not_called()

    @patch("game.get_hint")
    @patch('game.get_user_guess') 
    @patch("game.random.randint")
    def test_play_round_returns_none_after_all_wrong_guesses_and_calls_get_hint(self, mocked_no_to_be_guessed, mocked_user_guess, mocked_get_hint):
        mocked_user_guess.side_effect = [2,3,4]
        mocked_no_to_be_guessed.return_value = 1
        # user always declines hints hence return_value not side_effect so chances remain 3
        mocked_get_hint.return_value = 3
        attempts = game.play_round(difficulty=3,rounds=1) # chances 3
        self.assertIsNone(attempts)
        self.mocked_print.assert_any_call("You ran out of chances")
        self.assertEqual(mocked_get_hint.call_count, 1)
        mocked_get_hint.assert_called_with(3, 1, 2)

    @patch("game.display_summary")
    @patch("game.wants_another_round")
    @patch("game.play_round")
    @patch("game.select_difficulty")
    @patch("game.display_welcome_message") 
    def test_main_as_an_orchestrator(self, mocked_display_welcome, mocked_select_difficulty, mocked_play_round, mocked_play_another_round, mocked_display_summary):
        mocked_select_difficulty.return_value = 2
        mocked_play_round.return_value = 1
        mocked_play_another_round.return_value = False
        game.main()
        mocked_display_welcome.assert_called_once()
        mocked_select_difficulty.assert_called_once_with(1)
        # make sure the value returned from select_difficulty is what is inputted in play_round
        mocked_play_round.assert_called_with(2, 1)
        # test that high_score is appropriately updated
        mocked_display_summary.assert_called_with(1,{
        1: math.inf,
        2: 1,
        3: math.inf
    })
        # no need to reach into main() to inspect local variables game.main.high_scores
        # Also we don't need to initialize high_scores in the test either. main() initializes it itself.

    @patch("game.display_summary")
    @patch("game.wants_another_round")
    @patch("game.play_round")
    @patch("game.select_difficulty")
    def test_main_increments_round_when_player_plays_again(self, mocked_select_difficulty, mocked_play_round,mocked_play_another_round, mocked_display_summary):
        mocked_select_difficulty.side_effect = [1, 3]
        mocked_play_round.side_effect = [2, 1]
        mocked_play_another_round.side_effect = [True, False]

        game.main()

        mocked_select_difficulty.assert_has_calls([
            call(1),
            call(2)
        ])

        mocked_play_round.assert_has_calls([
            call(1, 1),
            call(3, 2)
        ])

        mocked_display_summary.assert_called_once_with(2,
            {
                1: 2,
                2: math.inf,
                3: 1
            }
        )

    @patch("game.display_summary")
    @patch("game.wants_another_round")
    @patch("game.play_round")
    @patch("game.select_difficulty")
    def test_main_does_not_update_high_score_when_round_is_lost(self,mocked_select_difficulty,mocked_play_round,mocked_play_another_round,mocked_display_summary):
        mocked_select_difficulty.return_value = 2
        mocked_play_round.return_value = None
        mocked_play_another_round.return_value = False

        game.main()

        mocked_display_summary.assert_called_once_with(1,
            {
                1: math.inf,
                2: math.inf,
                3: math.inf
            }
        )

if __name__ == "__main__":
    unittest.main()