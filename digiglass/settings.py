from .constants import SETTINGS_FILE, DEFAULT_SETTINGS_FILE

import yaml

import os
import shutil


ARG_NAMES = {
    'in_stock': 'stock',
    'lead_free': 'pbfree',
    'rohs_compliant': 'rohs',
    'sort_by': 'ColumnSort',
    'min_quantity': 'quantity'
}
BOOLEANS = ['stock', 'pbfree', 'rohs']


def _dotfile():
    with open(SETTINGS_FILE) as f:
        return yaml.load(f.read())


def create_config(force=False):
    """
    Create the default ~/.digiglass file if it doesn't already exist.
    Set force=True to erase the existing file and replace it with the default.
    """
    file_exists = os.path.isfile(SETTINGS_FILE)
    if (not file_exists) or force:
        shutil.copyfile(DEFAULT_SETTINGS_FILE, SETTINGS_FILE)


def default_filter_name():
    dotfile = _dotfile()
    return dotfile['settings']['default_filter']


def available_filter_names():
    dotfile = _dotfile()
    return dotfile['filters'].keys()


def get_filter(filter_name):
    dotfile = _dotfile()
    default_filter = dotfile['filters'][default_filter_name()]

    if filter_name is None:
        user_filter = {}
    else:
        user_filter = dotfile['filters'][filter_name]

    # Replace unset fields with values from the default filter
    result_filter = {}
    for key, default in default_filter.items():
        # Mutate key names into Digi-Key keyword args
        new_key = ARG_NAMES[key]
        result_filter[new_key] = user_filter.get(key, default)

    for key in BOOLEANS:
        # Replace booleans args with get query param values
        if result_filter[key]:
            result_filter[key] = '1'
        else:
            result_filter[key] = '0'

    return result_filter
