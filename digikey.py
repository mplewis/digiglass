#!/usr/bin/env python3

"""
Digi-Key terminal search engine.

Usage:
    digikey KEYWORDS...
    digikey --category CAT_NAME KEYWORDS...
    digikey --clear-cache

Options:
    --category CAT_NAME     Search for products in a specific Digi-Key category,
                            e.g. "Battery Chargers", "led discrete".
                            Supports fuzzy search.
    --clear-cache           Clears local data cached from Digi-Key. Data expires
                            on its own every 15 minutes, even if not cleared
                            manually.
"""

import requests
import appdirs
from bs4 import BeautifulSoup
from docopt import docopt
from fuzzywuzzy import process
from getch import getch
from colored import fg, attr
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

import re
import sys


APP_NAME = 'digiglass'
APP_AUTHOR = 'mplewis'
MAX_CATEGORIES = 20

CACHE_OPTS = {
    'cache.type': 'file',
    'cache.data_dir': appdirs.user_cache_dir(APP_NAME, APP_AUTHOR) + '/data',
    'cache.lock_dir': appdirs.user_cache_dir(APP_NAME, APP_AUTHOR) + '/lock',
    'cache.expire': 900  # 15 minutes
}
CACHE_MANAGER = CacheManager(**parse_cache_config_options(CACHE_OPTS))
CATEGORY_CACHE = CACHE_MANAGER.get_cache('category')
LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:MAX_CATEGORIES]


class Category:
    """A Digi-Key product category."""
    def __init__(self, id, name, parent, qty):
        self.id = id
        self.name = name
        self.parent = parent
        self.qty = qty

    def __repr__(self):
        return ('<Category {}: {} - {} ({} items)>'
                .format(self.id, self.parent, self.name, self.qty))


def parse_categories(page_tree):
    """
    Convert a BeautifulSoup tree for a Digi-Key page with a list of product
    categories into a list of Category objects.
    """
    prods = page_tree.find(id='productIndexList')
    categories = prods.find_all(class_='catfilteritem')
    cat_items = []

    for category in categories:
        parent = category.find(class_='catfiltertopitem').text.strip('\r\n\t')
        cat_sub = category.find(class_='catfiltersub')
        cat_item_trees = cat_sub.find_all('li')

        link_matcher = re.compile(r'^/product-search/en/.+/.+/(\d+)(.+)?$')
        text_matcher = re.compile(r'^(.+) \((\d+) items\)$')

        for item in cat_item_trees:
            raw_text = item.text.strip()
            link = item.find('a')['href']

            name, qty = text_matcher.match(raw_text).groups()
            id = int(link_matcher.match(link).groups()[0])

            cat_items.append(Category(id, name, parent, qty))

    return cat_items


def _all_categories():
    cats_tree = get_as_bs_tree('http://www.digikey.com/product-search/en')
    categories = parse_categories(cats_tree)
    return categories


def all_categories():
    return CATEGORY_CACHE.get(key='all_categories', createfunc=_all_categories)


def _categories_for_keyword(keyword):
    params = {'keywords': keyword}
    cats_tree = get_as_bs_tree('http://www.digikey.com/product-search/en',
                               params=params)
    categories = parse_categories(cats_tree)
    categories.sort(key=lambda c: c.qty, reverse=True)
    return categories


def categories_for_keyword(keyword):
    key = 'category.{}'.format(keyword)
    to_call = lambda: _categories_for_keyword(keyword)
    return CATEGORY_CACHE.get(key=key, createfunc=to_call)


def get_as_bs_tree(*args, **kwargs):
    """
    Retrieve a page using Requests and return its BeautifulSoup
    representation.
    """
    return BeautifulSoup(requests.get(*args, **kwargs).text)


def _category_fuzzy_name(category):
    """
    Strip non-alphanumerics from a category parent and name and lowercase it for
    use with fuzzy search.
    """
    hyphenated = '{} - {}'.format(category.parent, category.name)
    alphanumeric_only = re.sub(r'\W+', ' ', hyphenated)
    return alphanumeric_only.lower()


def closest_categories(search_term, categories, limit=MAX_CATEGORIES):
    results = process.extract(search_term, categories,
                              processor=_category_fuzzy_name, limit=limit)
    return [category for (category, _) in results[:limit]]


def getkey(message):
    print('{}: '.format(message), end='')
    sys.stdout.flush()
    answer = getch()
    print(answer)
    return answer


def get_user_category(categories):
    lookup = dict(zip(LETTERS, categories))
    longest = 0
    for category in lookup.values():
        digits = len(str(category.qty))
        if digits > longest:
            longest = digits
    for letter, category in sorted(lookup.items(), key=lambda t: t[0]):
        print('{}{}{}. ({}{}{}) {}{}{} - {}{}{}'.format(
              fg('red'), letter, attr('reset'),
              fg('blue'), str(category.qty).rjust(longest), attr('reset'),
              fg('green'), category.parent, attr('reset'),
              fg('yellow'), category.name, attr('reset')))
    found = None
    while not found:
        try:
            key = getkey('Select a category')
            found = lookup[key.lower()]
        except KeyError:
            print('Invalid selection.')
    return found


def main():
    args = docopt(__doc__)

    clear_cache = args['--clear-cache']
    dirty_cat = args['--category']
    search_term = ' '.join(args['KEYWORDS'])

    if clear_cache:
        CATEGORY_CACHE.clear()
        print('Cache cleared.')
        return

    if dirty_cat:
        # Search with category
        suggested_cats = closest_categories(dirty_cat, all_categories())
        clean_cat = get_user_category(suggested_cats)
        print(clean_cat)

    else:
        # Pick categories from search keyword
        suggested_cats = categories_for_keyword(search_term)
        clean_cat = get_user_category(suggested_cats)
        print(clean_cat)


if __name__ == '__main__':
    main()
