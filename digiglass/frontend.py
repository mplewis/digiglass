"""Everything that deals with user input."""

from constants import LETTERS

from colored import fg, attr
from getch import getch

import sys
import webbrowser
import urllib


def getkey(message):
    """Get one key from the user."""
    print('{}: '.format(message), end='')
    sys.stdout.flush()
    answer = getch()
    print(answer)
    return answer


def get_user_category(categories):
    """Ask the user to pick a part category from a list."""
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


def open_digikey(category, search_term):
    """Open a browser to the Digi-Key search page for the given arguments."""
    args = {
        'ColumnSort': 1000011,
        'stock': 1,
        'pbfree': 1,
        'rohs': 1,
        'quantity': 1
    }
    if search_term is not None:
        args['k'] = search_term
    args_encoded = urllib.parse.urlencode(args)
    url = ('http://www.digikey.com/product-search/en/a/a/{}?{}'
           .format(category.id, args_encoded))
    webbrowser.open(url)
