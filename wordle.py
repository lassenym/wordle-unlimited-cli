import sqlite3, os, shutil

RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
ORANGE = "\033[38;5;214m"


def db_connect():
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "wordle.db"))
    return conn, conn.cursor()  

def print_clues(guesses, answer):

    for guess in guesses:
        clue = [""] * 5
        remaining_letters = list(answer)

        for i, letter in enumerate(guess):
            if letter == answer[i]:
                clue[i] = f"{GREEN}{letter}{RESET}"
                remaining_letters[i] = None

        for i, letter in enumerate(guess):
            
            if clue[i] == "":
                if letter in remaining_letters:
                    clue[i] = f"{ORANGE}{letter}{RESET}"
                    remaining_letters[remaining_letters.index(letter)] = None
                else:
                    clue[i] = f"{RED}{letter}{RESET}"
        
        print(''.join(clue))
    
    print("=======================================================")

def game():
    conn, cursor = db_connect()

    answer = cursor.execute("SELECT * FROM answer_words ORDER BY RANDOM() LIMIT 1;").fetchall()[0][0]
    valid_guesses = [row[0] for row in cursor.execute("SELECT * FROM valid_words").fetchall()]
    guesses = []
    conn.close()

    while True:

        guess = input().upper()

        if len(guess) != 5:
            print(f"{RED}Only 5-letter words are allowed! Try again!{RESET}")        
            continue
        if guess not in valid_guesses:
            print(f"{ORANGE}Not a valid word! Try again!{RESET}")
            continue

        guesses.append(guess)
        for _ in range(shutil.get_terminal_size().lines):
            print()
        print_clues(guesses, answer)
        
        if guess == answer:
            print(f"{GREEN}You win! :){RESET}")
            break
        if len(guesses) > 5:
            print(f"{RED}You lose! :({RESET}")  
            break
        
if __name__ == "__main__":
    game()