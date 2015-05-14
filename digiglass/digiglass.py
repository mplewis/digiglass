#!/usr/bin/env python3

"""
Digiglass - Search Digi-Key from your terminal

Usage:
    digiglass KEYWORDS...
    digiglass --category CAT_NAME
    digiglass --category CAT_NAME KEYWORDS...
    digiglass --clear-cache

Options:
    -c CAT_NAME, --category CAT_NAME
        Search for products in a specific Digi-Key category, e.g.
        "Battery Chargers", "ceramic cap". Supports fuzzy search.
    --clear-cache
        Clears local data cached from Digi-Key. Data expires on its own every
        15 minutes, even if not cleared manually.
"""

from processing import closest_categories
from backend import all_categories, categories_for_keyword, clear_cache
from frontend import get_user_category, open_digikey

from docopt import docopt


def main():
    """Parse arguments and perform the search."""
    args = docopt(__doc__)

    do_clear_cache = args['--clear-cache']
    dirty_cat = args['--category']
    search_term = ' '.join(args['KEYWORDS']) or None

    if do_clear_cache:
        clear_cache()
        print('Cache cleared.')
        return

    if dirty_cat:
        # Search with category
        suggested_cats = closest_categories(dirty_cat, all_categories())
        clean_cat = get_user_category(suggested_cats)

    else:
        # Pick categories from search keyword
        suggested_cats = categories_for_keyword(search_term)
        clean_cat = get_user_category(suggested_cats)

    open_digikey(clean_cat, search_term)


if __name__ == '__main__':
    main()
