#!/usr/bin/env python3

"""
Digi-Key terminal search engine.

Usage:
    digikey KEYWORDS...
    digikey --category CAT_NAME KEYWORDS...

Options:
    --category CAT_NAME     The name of a Digi-Key category, e.g.
                            "Battery Chargers", "led discrete".
                            Supports fuzzy search.
"""

import requests
from bs4 import BeautifulSoup
from docopt import docopt

import re


prods_raw = requests.get('http://www.digikey.com/product-search/en').text


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


def get_as_bs_tree(*args, **kwargs):
    """
    Retrieve a page using Requests and return its BeautifulSoup
    representation.
    """
    return BeautifulSoup(requests.get(*args, **kwargs).text)


if __name__ == '__main__':
    args = docopt(__doc__)
    category = args['--category']
    search_term = ' '.join(args['KEYWORDS'])
    if category:
        print('Searching for {} in {}'.format(search_term, category))
    else:
        print('Searching for {}, no category given'.format(search_term))
