import re

def map_categories_to_index(categories: list[str],
                            categories_indexes: dict[str,int]) -> list[int]:
    """
    This function maps the NYTimes Sections with an index that
    represents the position of that section in the filter
    """
    if "Any" in categories:
        return [0]
    tmp_categories_indexes = []
    for category in categories:
        tmp_categories_indexes.append(categories_indexes[category])
    return tmp_categories_indexes


def normalize_months_to_watch(num_of_months: int):
    """
    This function returns the months number to search the news
    in the past
    """
    if num_of_months <= 1:
        return 0
    return num_of_months - 1


def find_dollar_ocurrence(phrase: str):
    """
    This function receives a text and checks if contains any pattern
    related to money or dollars specifically
    """
    any_word_pattern = "[a-zA-Z0-9.,\(\) ]*"
    dollar_pattern = "(\$[ ]?[1-9]+[0-9]*|[1-9]+[0-9]*[ ]?(USD|dollars))"
    phrase_dollar_pattern = any_word_pattern + dollar_pattern + any_word_pattern

    result = re.match(phrase_dollar_pattern, phrase)
    if result:
        return True
    return False
