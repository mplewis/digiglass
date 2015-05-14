from .constants import SETTINGS_FILE

import yaml


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
