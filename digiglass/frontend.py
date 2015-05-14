"""Everything that deals with user input."""

from .constants import LETTERS

from colored import fg, attr

import sys
import webbrowser
import urllib


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
            key = input('Select a category: ')
            found = lookup[key.strip().lower()]
        except KeyError:
            print('Invalid selection.')
        except KeyboardInterrupt:
            sys.exit(0)
    return found


def open_digikey(category, search_term, args):
    """Open a browser to the Digi-Key search page for the given arguments."""
    if search_term is not None:
        args['k'] = search_term
    args_encoded = urllib.parse.urlencode(args)
    url = ('http://www.digikey.com/product-search/en/a/a/{}?{}'
           .format(category.id, args_encoded))
    webbrowser.open(url)
