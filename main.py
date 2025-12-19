# ==================================================
# main.py (Beginner Friendly Version)
# ==================================================

import tkinter as tk
from tkinter import messagebox
import os
import game_logic
import words_list
from PIL import Image, ImageTk


# ==================================================
# CONFIGURATION VARIABLES
# ==================================================
HANGMAN_SIZE = (300, 300)          # Standard size for hangman images
BUTTON_SIZE = (150, 80)            # Size for button images
WINDOW_WIDTH = 600                  # Fixed window width
WINDOW_HEIGHT = 650                 # Fixed window height


# ==================================================
# GLOBAL VARIABLES
# ==================================================
root = None

# Images
hangman_images = []
hint_button_img = None
new_game_button_img = None

# Labels
hangman_label = None
hint_display_label = None
display_word_label = None
message_label = None
moves_label = None
final_status_label = None

# Entry and Buttons
guess_entry = None
guess_button = None
hint_button = None


# ==================================================
# FUNCTION: LOAD IMAGES
# ==================================================
def load_images():
    """
    Load hangman images and button images.
    Resize them to fit the window using PIL.
    """

    global hangman_images, hint_button_img, new_game_button_img

    # Load Hangman Images (0 to 6)
    for i in range(7):
        image_path = os.path.join("images", f"hangman{i}.png")
        try:
            pil_img = Image.open(image_path)
            pil_img = pil_img.resize(HANGMAN_SIZE, Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(pil_img)
            hangman_images.append(tk_img)
        except:
            hangman_images.append(None)

    # Load Hint Button Image
    try:
        pil_hint = Image.open(os.path.join("buttons", "hint_button.png"))
        pil_hint = pil_hint.resize(BUTTON_SIZE, Image.Resampling.LANCZOS)
        hint_button_img = ImageTk.PhotoImage(pil_hint)

        pil_new = Image.open(os.path.join("buttons", "newgame_button.png"))
        pil_new = pil_new.resize(BUTTON_SIZE, Image.Resampling.LANCZOS)
        new_game_button_img = ImageTk.PhotoImage(pil_new)

    except:
        hint_button_img = None
        new_game_button_img = None


# ==================================================
# FUNCTION: UPDATE UI ON GUESS
# ==================================================
def update_ui_on_guess(status):
    """
    Update the UI based on the result of a guess:
    - Update word display
    - Update attempts left
    - Update hangman image if incorrect
    - Show messages
    """

    # Update the masked word
    display_word_label.config(text=game_logic.get_display_word())

    # Update attempts left
    moves_label.config(text=f"Attempts Left: {game_logic.remaining_attempts}")

    # Show message based on guess
    if status == "correct":
        message_label.config(text="Correct Guess!", fg="green")

    elif status == "incorrect":
        message_label.config(text="Incorrect Guess! Attempt used.", fg="red")

        # Update hangman image
        stage = game_logic.max_attempts - game_logic.remaining_attempts
        if stage >= 0 and stage < len(hangman_images):
            hangman_label.config(image=hangman_images[stage])

    elif status == "already_guessed":
        message_label.config(text="Letter already used.", fg="blue")

    # Clear the input box
    guess_entry.delete(0, tk.END)

    # Check win/lose
    if status == "win":
        end_game(True)
    elif status == "lose":
        end_game(False)


# ==================================================
# FUNCTION: END GAME
# ==================================================
def end_game(is_win):
    """
    Stop the game and show final message.
    Disable input and buttons.
    """

    # Disable entry and buttons
    guess_entry.config(state=tk.DISABLED)
    guess_button.config(state=tk.DISABLED)
    hint_button.config(state=tk.DISABLED)

    if is_win:
        message_label.config(text="🎉 CONGRATULATIONS! YOU WON! 🎉", fg="blue")
        final_status_label.config(text="YOU DID IT!", fg="green")

    else:
        # Show full hangman image
        if len(hangman_images) > 6:
            hangman_label.config(image=hangman_images[6])

        # Show correct word
        correct_word = game_logic.word.upper()
        display_word_label.config(text=f'hidden word was: "{correct_word}"')

        # Show lose messages
        message_label.config(text="💔 GAME OVER! You ran out of attempts. 💔", fg="red")
        final_status_label.config(text="G A M E   O V E R", fg="red")


# ==================================================
# FUNCTION: HANDLE GUESS BUTTON
# ==================================================
def handle_guess():
    """
    Get the user's input and process it as a guess.
    """

    user_input = guess_entry.get().strip().lower()

    # Validate input
    if len(user_input) != 1 or not ('a' <= user_input <= 'z'):
        message_label.config(text="Please enter a single letter (A-Z).", fg="orange")
        guess_entry.delete(0, tk.END)
        return

    # Process the guess
    result = game_logic.guess_letter(user_input)

    # Update the UI
    update_ui_on_guess(result)


# ==================================================
# FUNCTION: HANDLE HINT BUTTON
# ==================================================
def handle_hint():
    """
    Provide a hint to the player.
    """

    result = game_logic.use_hint()

    if result is None:
        messagebox.showinfo("Hint", "No more extra hints available!")
        hint_button.config(state=tk.DISABLED)

    elif result == "game_over":
        messagebox.showinfo("Hint Used", "Used last attempt for a hint. Game Over.")
        if len(hangman_images) > 6:
            hangman_label.config(image=hangman_images[6])
        end_game(False)

    else:
        # Show hint
        current_hint = hint_display_label.cget("text")
        new_hint = current_hint + " | " + result
        hint_display_label.config(text=new_hint)
        messagebox.showinfo("Hint Used", f"New Hint: {result}\n(1 attempt lost)")

        # Update attempts and hangman image
        update_ui_on_guess("incorrect")

        # Disable hint if used 3 times
        if game_logic.hint_index >= 3:
            hint_button.config(state=tk.DISABLED)


# ==================================================
# FUNCTION: START NEW GAME FLOW
# ==================================================
def start_game_flow():
    """
    Initialize game state and update UI for a new game.
    """

    game_logic.start_new_game(words_list.hints_dict)

    # Show starting hint
    hint_display_label.config(text=f"Hint: {game_logic.starting_hint}")

    # Show masked word
    display_word_label.config(text=game_logic.get_display_word())

    # Show empty hangman
    if len(hangman_images) > 0:
        hangman_label.config(image=hangman_images[0])

    # Reset messages and moves
    message_label.config(text="Guess a letter to begin!", fg="black")
    final_status_label.config(text="")
    moves_label.config(text=f"Attempts Left: {game_logic.remaining_attempts}")

    # Enable input
    guess_entry.config(state=tk.NORMAL)
    guess_entry.delete(0, tk.END)
    guess_button.config(state=tk.NORMAL)
    hint_button.config(state=tk.NORMAL)


# ==================================================
# FUNCTION: CREATE MAIN WINDOW
# ==================================================
def create_main_window():
    """
    Setup main Tkinter window and all widgets.
    """

    global root
    global hangman_label, hint_display_label, display_word_label
    global message_label, moves_label, final_status_label
    global guess_entry, guess_button, hint_button

    # Root Window
    root = tk.Tk()
    root.title("Professional Hangman Game")
    root.config(bg="white")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    # Load Images
    load_images()

    # Frames
    top_frame = tk.Frame(root, bg="white", padx=10, pady=5)
    top_frame.pack(fill=tk.X)

    center_frame = tk.Frame(root, bg="white", padx=20, pady=10)
    center_frame.pack(pady=10)

    bottom_frame = tk.Frame(root, bg="white", padx=10, pady=10)
    bottom_frame.pack(fill=tk.X, expand=True)

    # Top Frame Widgets
    hint_display_label = tk.Label(top_frame, text="Hint: ", font=("Arial", 12, "bold italic"),
                                  bg="white", fg="#555555", wraplength=450, justify=tk.LEFT, anchor=tk.W)
    hint_display_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 20))

    moves_label = tk.Label(top_frame, text="Attempts Left: 7", font=("Arial", 12, "bold"),
                           bg="white", fg="#333333")
    moves_label.pack(side=tk.RIGHT)

    # Center Frame Widgets
    hangman_label = tk.Label(center_frame, image=hangman_images[0], bg="white")
    hangman_label.pack()

    final_status_label = tk.Label(center_frame, text="", font=("Arial", 16, "bold"), bg="white")
    final_status_label.pack(pady=5)

    # Bottom Frame Widgets
    input_word_frame = tk.Frame(bottom_frame, bg="white")
    input_word_frame.pack(pady=(0, 10))

    display_word_label = tk.Label(input_word_frame, text="_ _ _ _ _ _",
                                  font=("Courier", 28, "bold"), bg="white", fg="#333333")
    display_word_label.pack(side=tk.LEFT, padx=5)

    guess_entry = tk.Entry(input_word_frame, width=2, font=("Arial", 22), justify='center', bd=3, relief=tk.RIDGE)
    guess_entry.pack(side=tk.LEFT, padx=10)
    guess_entry.bind("<Return>", lambda event: handle_guess())

    guess_button = tk.Button(input_word_frame, text="GUESS", command=handle_guess,
                             font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", bd=3)
    guess_button.pack(side=tk.LEFT, padx=5)

    hint_button = tk.Button(bottom_frame,
                            image=hint_button_img if hint_button_img else None,
                            text="HINT" if not hint_button_img else "",
                            compound=tk.CENTER,
                            command=handle_hint,
                            font=("Arial", 10, "bold"),
                            bd=0,
                            relief=tk.FLAT)
    hint_button.pack(side=tk.LEFT, padx=10)

    new_game_button = tk.Button(bottom_frame,
                                image=new_game_button_img if new_game_button_img else None,
                                text="NEW GAME" if not new_game_button_img else "",
                                compound=tk.CENTER,
                                command=start_game_flow,
                                font=("Arial", 10, "bold"),
                                bd=0,
                                relief=tk.FLAT)
    new_game_button.pack(side=tk.RIGHT, padx=10)

    message_label = tk.Label(bottom_frame, text="Welcome! Press 'New Game' to start.",
                             font=("Arial", 10), fg="black", bg="white")
    message_label.pack(pady=(10, 0))

    # Start the game
    start_game_flow()

    # Mainloop
    root.mainloop()


# ==================================================
# APPLICATION ENTRY POINT
# ==================================================
if __name__ == "__main__":
    create_main_window()
