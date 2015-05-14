"""Everything that deals with access to digikey.com and data caching."""

from .constants import APP_NAME, APP_AUTHOR, CACHE_EXPIRY
from .parsing import get_as_bs_tree, parse_categories

import appdirs
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


CACHE_DIR = appdirs.user_cache_dir(APP_NAME, APP_AUTHOR)
CACHE_OPTS = {
    'cache.type': 'file',
    'cache.data_dir': CACHE_DIR + '/data',
    'cache.lock_dir': CACHE_DIR + '/lock',
    'cache.expire': CACHE_EXPIRY
}
CACHE_MANAGER = CacheManager(**parse_cache_config_options(CACHE_OPTS))
CATEGORY_CACHE = CACHE_MANAGER.get_cache('category')


def clear_cache():
    CATEGORY_CACHE.clear()


def _all_categories():
    """Cache helper for all_categories."""
    cats_tree = get_as_bs_tree('http://www.digikey.com/product-search/en')
    categories = parse_categories(cats_tree)
    return categories


def all_categories():
    """Get all Digi-Key categories."""
    return CATEGORY_CACHE.get(key='all_categories', createfunc=_all_categories)


def _categories_for_keyword(keyword):
    """Cache helper for categories_for_keyword."""
    params = {'keywords': keyword}
    cats_tree = get_as_bs_tree('http://www.digikey.com/product-search/en',
                               params=params)
    categories = parse_categories(cats_tree)
    categories.sort(key=lambda c: c.qty, reverse=True)
    return categories


def categories_for_keyword(keyword):
    """Get the categories with the most parts for the given keyword."""
    key = 'category.{}'.format(keyword)
    to_call = lambda: _categories_for_keyword(keyword)
    return CATEGORY_CACHE.get(key=key, createfunc=to_call)
