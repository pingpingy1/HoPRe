"""Helper functions for HoPRe"""

import os
import json
from string import punctuation
from swiplserver import PrologThread


def tokenize(phrase: str) -> list[str]:
    """Tokenizes the given phrase to a list of words.

    :param phrase: Phrase to tokenize
    :return: List of words in lowercase"""
    return phrase.strip().lower().translate(str.maketrans("", "", punctuation)).split()


def load_db_json(
    filename: str, related: list[str] | None = None, encoding: str = "UTF-8"
) -> set[tuple[str, str]]:
    """Fetches all pairs of phrases from the provided JSON file.

    :param filename: Name of JSON file encoding homophonic phrases
    :param related: Only phrases related to these phrases will be returned, if specified
    :param encoding: Encoding of JSON file
    :return: Set of pairs of homophonic phrases
    """
    pairs: set[tuple[str, str]] = set()

    if not os.path.isfile(filename):
        raise ValueError(f"No file named {filename}")

    with open(filename, "r", encoding=encoding) as f:
        json_obj: list[dict[str, str]] = json.load(f)

    for pair in json_obj:
        for phrase1, phrase2 in pair.items():
            assert isinstance(phrase1, str)
            assert isinstance(phrase2, str)
            if (related is None) or (phrase1 in related) or (phrase2 in related):
                pairs.add((phrase1, phrase2))

    return pairs


def assert_all(
    pairs: set[tuple[str, str]],
    predicate: str,
    pthread: PrologThread,
    symmetric: bool = False,
) -> None:
    """Takes all pairs in the set and assert them with the given predicate.

    :param pairs: Set of pairs of strings to be asserted
    :param predicate: Name of the predicate to be asserted; must be declared as dynamic
    :param pthread: Prolog thread where assertions will happen
    :param symmetric: If set True, then every pair (A, B) will be asserted as (B, A) once more
    """
    for phrase1, phrase2 in pairs:
        p1_tok = tokenize(phrase1)
        p2_tok = tokenize(phrase2)
        pthread.query(f"assertz({predicate}({p1_tok}, {p2_tok}))")
        if symmetric:
            pthread.query(f"assertz({predicate}({p2_tok}, {p1_tok}))")


def assert_all_json(
    filename: str,
    predicate: str,
    pthread: PrologThread,
    related: list[str] | None = None,
    encoding: str = "UTF-8",
    symmetric: bool = False,
):
    """Takes all pairs in the JSON file and assert them with the given predicate.

    :param filename: Name of JSON file encoding homophonic phrases
    :param predicate: Name of the predicate to be asserted; must be declared as dynamic
    :param pthread: Prolog thread where assertions will happen
    :param related: Only phrases related to these phrases will be returned, if specified
    :param encoding: Encoding of JSON file
    :param symmetric: If set True, then every pair (A, B) will be asserted as (B, A) once more
    """
    assert_all(load_db_json(filename, related, encoding), predicate, pthread, symmetric)
