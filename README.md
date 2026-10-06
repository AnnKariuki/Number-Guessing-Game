# Number Guessing Game

A command-line number guessing game where the player tries to guess a randomly selected number between 1 and 100. The player is given a limited number of chances depending on the selected difficulty level.

This project is based on the [roadmap.sh Number Guessing Game project](https://roadmap.sh/projects/number-guessing-game).

## Features

- Select a difficulty level for each round:
  - Easy: 10 chances
  - Medium: 5 chances
  - Hard: 3 chances
- Play multiple rounds in a single session.
- Track how long it takes to correctly guess the number.
- Receive hints when stuck.
- Accepting a hint costs one chance.
- Track the best score for each difficulty level based on the fewest attempts.
- View a summary of high scores when the game ends.
- Input validation with a limited number of retries.

## Requirements

- Python 3

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## Usage

Run the game with:

```bash
python3 game.py
```

Follow the prompts to select a difficulty level and start guessing.

## Running Tests

Run the test suite with:

```bash
python3 -m unittest
```

## How the Game Works

At the beginning of each round, the program randomly selects a number between 1 and 100. The player selects a difficulty level, which determines the number of available chances. 
The player then enters guesses until they either guess the correct number or run out of chances. During the game, the player may request a hint. Accepting a hint costs one chance.
After a round ends, the player can choose to play another round. When the player quits, the game displays a summary containing the best score achieved for each difficulty level.