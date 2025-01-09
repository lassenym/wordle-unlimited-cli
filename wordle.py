import sqlite3, os, shutil

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
ORANGE = "\033[38;5;214m"
BLUE = "\033[34m"
GRAY = "\033[90m"

LAYOUT = [['Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P'], ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'], ['Y', 'X', 'C', 'V', 'B', 'N', 'M']]

def db_connect():
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "wordle.db"))
    return conn, conn.cursor()

def calc_guesses(guesses, answer):
    layout_dict = {key: '' for row in LAYOUT for key in row}
    clues = []

    for guess in guesses:
        remaining_letters = list(answer) 
        clue = [""] * len(answer)


        for i, letter in enumerate(guess):
            if letter == answer[i]:
                clue[i] = f"{GREEN}{letter}{RESET}"
                layout_dict[letter] = f"{GREEN}{letter}{RESET}"
                remaining_letters[i] = None  


        for i, letter in enumerate(guess):
            if clue[i]:
                continue

            if letter in remaining_letters:
                clue[i] = f"{ORANGE}{letter}{RESET}"  # Orange case
                layout_dict[letter] = f"{ORANGE}{letter}{RESET}"
                remaining_letters[remaining_letters.index(letter)] = None 
            else:
                clue[i] = f"{RED}{letter}{RESET}"
                if not layout_dict[letter]:
                    layout_dict[letter] = f"{RED}{letter}{RESET}"

        clues.append(''.join(clue))

    return layout_dict, clues


def print_clues(layout_dict, clues):

    print("\n" * (shutil.get_terminal_size().lines - 6 - len(clues)))
        
    for line in LAYOUT:
        print("\n                  " + ((10-len(line)) * " "), end="")
        for letter in line:
            if layout_dict[letter]:
                print(layout_dict[letter], end=" ")
            else:
                print(letter, end=" ")

    print()
    for clue in clues:
        print(clue)


    print("\n=======================================================")



def game():
    conn, cursor = db_connect()
    answer = cursor.execute("SELECT word FROM answer_words ORDER BY RANDOM() LIMIT 1;").fetchall()[0][0]
    valid_guesses = [row[0] for row in cursor.execute("SELECT word FROM valid_words").fetchall()]
    answer = "BUDGE"
    conn.close()

    guesses = []
    guessed_letters = []

    while True:

        guess = input().upper()

        if guess == 'EXIT' or guess == 'QUIT':
            exit()

        if len(guess) != 5:
            print(f"{RED}Only 5-letter words are allowed! Try again!{RESET}")        
            continue
        if guess not in valid_guesses:
            print(f"{ORANGE}Not a valid word! Try again!{RESET}")
            continue
        
        guesses.append(guess)
        print_clues(*calc_guesses(guesses, answer))

        if guess == answer:
            print(f"{GREEN}You win! :){RESET}")
            break
        if len(guesses) > 5:
            print(f"{RED}You lose! :({RESET} The word was {BLUE}{answer}{RESET}")  
            break

if __name__ == "__main__":
    print(f"{BLUE}Let's go! Start guessing:{RESET}\n")
    game()
