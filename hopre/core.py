"""User interface for HoPRe"""

import os

from swiplserver import PrologMQI


BASE_DIR = os.path.dirname(__file__)


def hopre() -> None:
    """The main HoPRe (Homophone-based Pun Recognition) function."""

    with PrologMQI() as mqi:
        with mqi.create_thread() as pthread:
            english_analyzer = os.path.join(BASE_DIR, "englishAnalysis", "lambda.pl")
            print(english_analyzer)
            pthread.query(f'consult("{english_analyzer}")')

            while True:
                os.system("clear")
                pthread.query_async("lambda")
                print(pthread.query_async_result())

                if input("Press enter to continue or q to exit...") == "q":
                    os._exit(0)


if __name__ == "__main__":
    hopre()
