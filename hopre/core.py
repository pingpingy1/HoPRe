"""User interface for HoPRe"""

import os
from swiplserver import PrologMQI, PrologThread
from hopre.utils import assert_all_json, tokenize


BASE_DIR = os.path.dirname(__file__)


def check_homonym_pun(sentence: list[str], pthread: PrologThread) -> bool:
    """Checks whether the provided sentence is a homonym-based pun.

    :param sentence: Tokenized sentence to be tested
    :param pthread: Prolog thread with predicates similar/2 and dissimilar/2 declared
    :return: True if the sentence satisfies the conditions for a homonym-based pun"""


def hopre() -> None:
    """The main HoPRe (Homophone-based Pun Recognition) function."""

    with PrologMQI() as mqi:
        with mqi.create_thread() as pthread:
            init_pl = os.path.join(BASE_DIR, "init.pl")
            pthread.query(f'consult("{init_pl}")')

            lambda_pl = os.path.join(BASE_DIR, "englishAnalysis", "lambda.pl")
            pthread.query(f'consult("{lambda_pl}")')

            detect_pl = os.path.join(BASE_DIR, "pun_detection.pl")
            pthread.query(f'consult("{detect_pl}")')

            homophone_json = os.path.join(BASE_DIR, "homophone_kb", "homophone.json")
            assert_all_json(homophone_json, "homophone", pthread, symmetric=True)

            similar_json = os.path.join(BASE_DIR, "context_kb", "similar.json")
            assert_all_json(similar_json, "similar", pthread, symmetric=True)

            dissimilar_json = os.path.join(BASE_DIR, "context_kb", "dissimilar.json")
            assert_all_json(dissimilar_json, "dissimilar", pthread, symmetric=True)

            while True:
                phrase = tokenize(input())
                print(phrase)
                print(pthread.query(f"homophone({phrase}, H)"))
                print(pthread.query(f"similar({phrase}, S)"))
                print(pthread.query(f"dissimilar({phrase}, D)"))
                print(pthread.query(f"lambda:t(_,{phrase},[])"))
                print(pthread.query(f"homonymPun([{phrase}])"))

                if input("Press enter to continue or q to exit...") == "q":
                    break


if __name__ == "__main__":
    hopre()
