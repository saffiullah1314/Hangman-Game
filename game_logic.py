import random

# Global variables
word = "" # this is used to store a word which is to be guessed
hints = [] # this is list which store hints
starting_hint = ""  # First hint shown automatically
extra_hints = []   # Extra hints for the player to use
hint_index = 0   # Counter for how many hints have been used

max_attempts = 6   # Maximum wrong guesses allowed
remaining_attempts = 6   # Remaining wrong guesses left


display = []  # Current display of the word (['_', '_', '_'])
used_letters = []  # Letters player has already guessed

def start_new_game(hints_dict):
    global word, hints, starting_hint, extra_hints
    global hint_index, remaining_attempts, display, used_letters

    # Reset everything
    remaining_attempts = max_attempts
    used_letters = []
    display = []
    hint_index = 0

    # Pick random word
    word = random.choice(list(hints_dict.keys()))
    hints = hints_dict[word]

    # First hint (starting hint)
    starting_hint = hints[0]

    # Remaining 3 hints for button
    extra_hints = hints[1:]

    # Display setup ("_ _ _ _")
    for i in range(len(word)):
        display.append("_")



# this function display the word in clear format like if diplay is display = ['a', 'p', 'p', '_', '_']....then with this function it will show like this "a p p _ _"
def get_display_word():
    """Returns the masked word with spaces like: p y _ h o n"""
    result = ""
    for letter in display:
        result += letter + " "
    return result.strip() #strip is a function which remove extra double spaces for example "  a p p _ _  " then with strip it will look "a p p _ _"


def guess_letter(letter):
    """Handles correct/wrong guesses."""
    global remaining_attempts

    letter = letter.lower()

    # Check already used
    if letter in used_letters:
        return "already_guessed"

    used_letters.append(letter)

    # Correct guess
    if letter in word:
        for i in range(len(word)):
            if word[i] == letter:
                display[i] = letter

        # Check if completed
        if "_" not in display:
            return "win"
        return "correct"

    # Wrong guess
    else:
        remaining_attempts -= 1

        if remaining_attempts <= 0:
            return "lose"

        return "incorrect"


def use_hint():
    """Returns next hint and reduces attempt."""
    global hint_index, remaining_attempts

    # No more hints left
    if hint_index >= 3:
        return None

    hint = extra_hints[hint_index]
    hint_index += 1

    # Reduce chance
    remaining_attempts -= 1

    if remaining_attempts <= 0:
        return "game_over"

    return hint
