"""User interface for HoPRe"""


import sys
import os


def hopre() -> None:
    """The main HoPRe (Homophone-based Pun Recognition) function."""
    while True:
        user_input: str = input("Please enter a sentence:\n")
        if user_input == "Goodbye.":
            print("It was a good run! Goodbye.")
            sys.exit()

        print(f"\nHere's the sentence you provided:\n{user_input}")
        input("Press enter to continue...")
        os.system("clear")


if __name__ == "__main__":
    hopre()
