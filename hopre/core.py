"""User interface for HoPRe"""

import os
from swiplserver import PrologMQI
from hopre.utils import assert_all_json, tokenize


BASE_DIR = os.path.dirname(__file__)


def hopre() -> None:
    """The main HoPRe (Homophone-based Pun Recognition) function."""

    with PrologMQI(output_file_name=os.path.join(BASE_DIR, "output.log")) as mqi:
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
                n = int(input("Please enter the number of sentences: "))
                print()
                print("Please enter the joke, one sentence at a time:")
                sentences = [tokenize(input()) for _ in range(n)]

                result = pthread.query(
                    f"homonymPun({sentences},HomonymPhrase,Context1,Context2)"
                )

                print()
                if result:
                    assert isinstance(result, list)
                    fst = result[0]
                    context1 = " ".join(fst["Context1"])
                    context2 = " ".join(fst["Context2"])
                    homonym = " ".join(fst["HomonymPhrase"])
                    print("I get it!")
                    print(
                        f'The two incompatible interpretations of "{context1}" and "{context2}" are resolved with the homonym "{homonym}"!'
                    )
                else:
                    print("I don't think this is a joke...")

                print()
                if input("Press enter to continue or q to exit...").endswith("q"):
                    break

                print()
                print()


if __name__ == "__main__":
    hopre()
