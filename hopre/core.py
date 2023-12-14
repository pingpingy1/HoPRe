"""User interface for HoPRe"""

import os, sys, getopt, json
from swiplserver import PrologMQI, PrologThread
from hopre.utils import assert_all_json, tokenize


BASE_DIR = os.path.dirname(__file__)


def init_kb(pthread: PrologThread) -> None:
    """Initialize knowledge bases in the given PrologTrhead."""
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


def get_user_input(num_sentences: int, prompt: str | None = None) -> list[list[str]]:
    """Get user's input of multiple sentences.

    :param prompt: Prompt to get user's inputs
    :param num_sentences: Number of sentences to get
    :return: List of tokenized input sentences
    """
    if prompt:
        print(prompt + "\n")

    ret = [tokenize(input()) for _ in range(num_sentences)]
    print()
    return ret


def check_homonym_pun(
    sentences: list[list[str]], pthread: PrologThread
) -> tuple[str, str, str] | None:
    """Checks whether the given sentences are a homonym-based pun.

    :param sentences: List of tokenized input sentences
    :param pthread: PrologThread where all required knowledge have been asserted
    :return: Analysis of the joke if it is a joke; None otherwise
    """
    result = pthread.query(f"homonymPun({sentences},HomonymPhrase,Context1,Context2)")
    if result:
        assert isinstance(result, list)
        fst = result[0]
        context1 = " ".join(fst["Context1"])
        context2 = " ".join(fst["Context2"])
        homonym = " ".join(fst["HomonymPhrase"])
        return (context1, context2, homonym)
    return None


def check_homophone_pun(
    sentences: list[list[str]], pthread: PrologThread
) -> tuple[str, str, str, str] | None:
    """Checks whether the given sentences are a homophone-based pun.

    :param sentences: List of tokenized input sentences
    :param pthread: PrologThread where all required knowledge have been asserted
    :return: Analysis of the joke if it is a joke; None otherwise
    """
    result = pthread.query(
        f"homophonePun({sentences},Homophone1,Homophone2,Context1,Context2)"
    )
    if result:
        assert isinstance(result, list)
        fst = result[0]
        context1 = " ".join(fst["Context1"])
        context2 = " ".join(fst["Context2"])
        homophone1 = " ".join(fst["Homophone1"])
        homophone2 = " ".join(fst["Homophone2"])

        return (context1, context2, homophone1, homophone2)
    return None


def check_pun(sentences: list[list[str]], pthread: PrologThread) -> tuple[str, bool]:
    """Checks whether the given sentences are a homophone-based pun.

    :param sentences: List of tokenized input sentences
    :param pthread: PrologThread where all required knowledge have been asserted
    :return: Return message of HoPRe to the given input
    """
    res1 = check_homonym_pun(sentences, pthread)
    if res1:
        context1, context2, homonym = res1
        return (
            "I get it!\n"
            + "The two incompatible interpretations of "
            + context1
            + " and "
            + context2
            + " are resolved with the homonym "
            + homonym
            + "!",
            True,
        )

    res2 = check_homophone_pun(sentences, pthread)
    if res2:
        context1, context2, homophone1, homophone2 = res2
        return (
            "I get it!\n"
            + "The two incompatible interpretations of "
            + context1
            + " and "
            + context2
            + " are resolved with the homophones "
            + homophone1
            + " and "
            + homophone2
            + "!",
            True,
        )

    return ("I don't think that is a joke...", False)


def hopre() -> None:
    """The main HoPRe (Homophone-based Pun Recognition) function."""

    with PrologMQI(output_file_name=os.path.join(BASE_DIR, "output.log")) as mqi:
        with mqi.create_thread() as pthread:
            init_kb(pthread)

            while True:
                n = int(input("Please enter the number of sentences: "))
                print()
                sentences = get_user_input(
                    n, "Please enter the joke, one sentence at a time:"
                )

                print()
                print(check_pun(sentences, pthread))
                print()

                if input("Press enter to continue or q to exit...").endswith("q"):
                    break

                print()
                print()


def test(filename: str | None = None, encoding: str = "UTF-8") -> None:
    """Perform all tests given in the JSON file.

    :param filename: Path to JSON file, if provided
    :param encoding: Encoding of JSON file
    """
    if not filename:
        filename = os.path.join(BASE_DIR, "punTestSuite.json")

    print(f"Running tests in {filename}...\n")

    with open(filename, "r", encoding=encoding) as f:
        testcases = json.load(f)

    assert isinstance(testcases, list)

    positive: int = 0
    positive_success: int = 0
    negative: int = 0
    negative_success: int = 0

    with PrologMQI(output_file_name=os.path.join(BASE_DIR, "output.log")) as mqi:
        with mqi.create_thread() as pthread:
            init_kb(pthread)

            for tc in testcases:
                assert "input" in tc.keys()
                assert "joke" in tc.keys()

                if tc["joke"]:
                    positive += 1
                else:
                    negative += 1

                sentences = [tokenize(s) for s in tc["input"]]
                result, hopre_ans = check_pun(sentences, pthread)

                if hopre_ans == tc["joke"]:
                    if tc["joke"]:
                        positive_success += 1
                    else:
                        negative_success += 1

                print(f'Provided input:\n{tc["input"]}')
                print(f'Answer: {"Pun" if tc["joke"] else "Not a pun"}')
                print(f'HoPRe: {"Pun" if hopre_ans else "Not a pun"}')
                if hopre_ans:
                    print(f"Analysis: {result}")
                print(f'Status: {"SUCCESS" if hopre_ans == tc["joke"] else "FAIL"}')
                print()

            print(f"Positive test: {positive_success} / {positive}")
            print(f"Negative test: {negative_success} / {negative}")


if __name__ == "__main__":
    opts, _ = getopt.getopt(sys.argv[1:], "t", ["test"])
    if opts:
        test()
    else:
        hopre()
