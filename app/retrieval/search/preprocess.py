import string

import nltk
from nltk.corpus import stopwords


# Download the NLTK stopword corpus automatically
# if it is not already available locally.

try:
    STOPWORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    STOPWORDS = set(stopwords.words("english"))


def preprocess_query(text: str) -> list[str]:
    """
    Preprocess a user query for lexical retrieval.

    Steps:
    1. Convert to lowercase.
    2. Remove punctuation.
    3. Split into words.
    4. Remove English stopwords.

    Args: Takes text as a string.
    Returns: A list of strings.
    """

    tokens = []

    for word in text.split():

        word = (
            word.lower()
            .strip(string.punctuation)
        )

        if not word:
            continue

        if word in STOPWORDS:
            continue

        tokens.append(word)

    return tokens