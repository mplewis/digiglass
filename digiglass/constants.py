from os.path import expanduser

SETTINGS_FILE = expanduser('~/.digiglass')
DEFAULT_SETTINGS_FILE = 'digiglass/resource/default_settings.yml'

APP_NAME = 'digiglass'
APP_AUTHOR = 'mplewis'
CACHE_EXPIRY = 900  # 15 minutes

# The max number of categories to display when asking the user to choose
MAX_CATEGORIES = 20

# Used for getting choices from the user
LETTERS = 'abcdefghijklmnopqrstuvwxyz'[:MAX_CATEGORIES]
