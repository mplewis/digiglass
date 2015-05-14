"""Everything dealing with filtering or matching based on user data."""

from constants import MAX_CATEGORIES

from fuzzywuzzy import process

import re


def _category_fuzzy_name(category):
    """
    Strip non-alphanumerics from a category parent and name and lowercase it for
    use with fuzzy search.
    """
    hyphenated = '{} - {}'.format(category.parent, category.name)
    alphanumeric_only = re.sub(r'\W+', ' ', hyphenated)
    return alphanumeric_only.lower()


def closest_categories(search_term, categories, limit=MAX_CATEGORIES):
    """
    Use fuzzy string matching to find the category closest to what the user was
    searching for.
    """
    results = process.extract(search_term, categories,
                              processor=_category_fuzzy_name, limit=limit)
    return [category for (category, _) in results[:limit]]
