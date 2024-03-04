from typing import Iterable


def pluralize(singular: str, plural: str, items: Iterable) -> str:
    """
    Select the singular or plural form of a word based on the number of items.

    :param singular: Singular form of the word.
    :param plural: Plural form of the word.
    :param items: Items to count.
    """

    return singular if len(items) == 1 else plural
