"""Everything that parses Digi-Key's HTML into usable data."""

from models import Category

import re

import requests
from bs4 import BeautifulSoup


def parse_categories(page_tree):
    """
    Convert a BeautifulSoup tree for a Digi-Key page with a list of product
    categories into a list of Category objects.
    """
    prods = page_tree.find(id='productIndexList')
    categories = prods.find_all(class_='catfilteritem')
    cat_items = []

    for category in categories:
        parent = category.find(class_='catfiltertopitem').text.strip()
        cat_sub = category.find(class_='catfiltersub')
        cat_item_trees = cat_sub.find_all('li')

        link_matcher = re.compile(r'^/product-search/en/.+/.+/(\d+)(.+)?$')
        text_matcher = re.compile(r'^(.+) \((\d+) items\)$')

        for item in cat_item_trees:
            if item.find('li'):
                # This item isn't valid, skip it
                # Digi-Key doesn't close all their li tags
                # Closing li tag is optional but it messes up BS
                continue

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
    html = requests.get(*args, **kwargs).text
    return BeautifulSoup(html)
