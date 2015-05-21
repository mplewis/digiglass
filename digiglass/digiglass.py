#!/usr/bin/env python3

"""
Digiglass - Search Digi-Key from your terminal

Usage:
    digiglass [-f FILTER] [-c CATEGORY] KEYWORDS...
    digiglass [-f FILTER] -c CATEGORY
    digiglass --list-filters
    digiglass --reset-config
    digiglass --clear-cache

Options:
    -c CATEGORY, --category CATEGORY
        Search for products in a specific Digi-Key category, e.g.
        "Battery Chargers", "ceramic cap". Supports fuzzy search.
    -f FILTER, --filter FILTER
        Specify a filter. If no filter is specified, the default filter is used.
        Configure filters in the ~/.digiglass file.
    --list-filters
        List all available filters.
    --reset-config
        Resets your ~/.digiglass config file to the default.
    --clear-cache
        Clears local data cached from Digi-Key. Data expires on its own every
        15 minutes, even if not cleared manually.
"""

from .processing import closest_categories
from .backend import all_categories, categories_for_keyword, clear_cache
from .frontend import get_user_category, open_digikey
from .settings import (available_filter_names, get_filter, default_filter_name,
                       create_config)

from docopt import docopt

import sys


def main():
    """Parse arguments and perform the search."""
    create_config()

    args = docopt(__doc__)

    list_filters = args['--list-filters']
    reset_config = args['--reset-config']
    do_clear_cache = args['--clear-cache']
    dirty_cat = args['--category']
    search_term = ' '.join(args['KEYWORDS']) or None
    filter_name = args['--filter']

    if reset_config:
        create_config(force=True)
        print('Config file reset to defaults.')
        return

    if do_clear_cache:
        clear_cache()
        print('Cache cleared.')
        return

    if list_filters:
        print('Available filters: {}'
              .format(', '.join(available_filter_names())))
        print('Default filter: {}'.format(default_filter_name()))
        return

    if dirty_cat:
        # Search with category
        suggested_cats = closest_categories(dirty_cat, all_categories())
        clean_cat = get_user_category(suggested_cats)

    else:
        # Pick categories from search keyword
        suggested_cats = categories_for_keyword(search_term)

        if not suggested_cats:
            print('No items found for keyword(s) {}'.format(search_term))
            sys.exit(0)

        clean_cat = get_user_category(suggested_cats)

    user_filter = get_filter(filter_name)
    open_digikey(clean_cat, search_term, user_filter)


if __name__ == '__main__':
    main()
