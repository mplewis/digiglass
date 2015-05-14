from os.path import expanduser

from pkg_resources import resource_string

SETTINGS_FILE = expanduser('~/.digiglass')

APP_NAME = 'digiglass'
APP_AUTHOR = 'mplewis'
CACHE_EXPIRY = 900  # 15 minutes

# The max number of categories to display when asking the user to choose
MAX_CATEGORIES = 20

# Used for getting choices from the user
LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:MAX_CATEGORIES]


def DEFAULT_SETTINGS():
    return resource_string(__name__, 'resource/default_settings.yml')
