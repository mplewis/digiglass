#!/usr/bin/env python3

"""
Digi-Key terminal search engine.

Usage:
    digikey KEYWORDS...
    digikey --category CAT_NAME KEYWORDS...

Options:
    --category CAT_NAME     Search for products in a specific Digi-Key category,
                            e.g. "Battery Chargers", "led discrete".
                            Supports fuzzy search.
"""

import requests
from bs4 import BeautifulSoup
from docopt import docopt
from fuzzywuzzy import process
from getch import getch
from colored import fg, attr

import re
import sys


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


def all_categories():
    cats_tree = get_as_bs_tree('http://www.digikey.com/product-search/en')
    categories = parse_categories(cats_tree)
    return categories


def get_as_bs_tree(*args, **kwargs):
    """
    Retrieve a page using Requests and return its BeautifulSoup
    representation.
    """
    return BeautifulSoup(requests.get(*args, **kwargs).text)


def closest_categories(search_term, categories, limit=10):
    return [cat for (cat, score) in
            process.extract(search_term, categories,
                            processor=lambda c: c.name, limit=limit)]


def getkey(message):
    print('{}: '.format(message), end='')
    sys.stdout.flush()
    answer = getch()
    print(answer)
    return answer


def get_user_category(categories):
    letters = 'abcdefghijklmnopqrstuvwxyz'[:len(categories)]
    lookup = dict(zip(letters, categories))
    for letter, category in sorted(lookup.items(), key=lambda t: t[0]):
        print('{}{}{}. {}{}{} - {}{}{}'.format(
              fg('red'), letter, attr('reset'),
              fg('green'), category.parent, attr('reset'),
              fg('yellow'), category.name, attr('reset')))
    key = getkey('Select a category')
    return lookup[key.lower()]

if __name__ == '__main__':
    args = docopt(__doc__)
    dirty_cat = args['--category']
    search_term = ' '.join(args['KEYWORDS'])
    if dirty_cat:
        suggested_cats = closest_categories(search_term, all_categories())
        clean_cat = get_user_category(suggested_cats)
        print(clean_cat)
    else:
        print('Searching for {}, no category given'.format(search_term))
