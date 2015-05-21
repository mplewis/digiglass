# Digiglass

*Search Digi-Key from your terminal*

Searching Digi-Key can be a pain. Here's a list of things I do every time I search for an item:

* Filter by "In Stock"
* Filter by "Quantity Desired: 1"
* Sort by price, ascending

Each of those actions takes a click and a couple seconds to load. I can automate these tasks and do most of the work from the command line.

# Usage

* Search for blue LEDs:  
`digiglass blue led`
* Search for 470-ohm resistors in the through-hole category:  
`digiglass -c 'through hole resistor' 470 ohm`
* Browse all resistor kits:  
`digiglass --category 'resistor kit'`

`-c` and `--category` are interchangeable. Category names support fuzzy search - you can type part of the name and the proper category will probably appear.

# Installation

This is a Python 3 script, so use `pip3` to install:

```
pip3 install digiglass
```

# Filters

Specify a filter to be used during a search like this: `digiglass --filter some_new_filter`

You can customize the filters used by Digiglass by modifying `~/.digiglass`. It's a YAML file that looks like this:

```
filters:
    my_filter:
        in_stock: true
        lead_free: false
        rohs_compliant: false
        sort_by: '1000011'  # Unit price, USD, ascending
        min_quantity: 1
    pb_rohs:
        lead_free: true
        rohs_compliant: true

settings:
    default_filter: my_filter
```

Valid options are:

* `in_stock`: Item must be in stock
* `lead_free`: Item must be lead free
* `rohs_compliant`: Item must be RoHS compliant
* `sort_by`: The column by which to sort results
* `min_quantity`: At least this many of this item must be available

Every field in a filter is optional.

`default_filter` is used when no filter is specified.

Fields not specified in a requested filter use the default filter's settings.

# Troubleshooting

Having issues? Try clearing the app's cache: `digiglass --clear-cache`

Still having issues? Odds are Digi-Key changed their HTML format. They probably broke the app's screen scraping. Let me know and I'll try and fix it—or dig in yourself! Screen scraping is fun.

# Contributions

Bug reports, fixes, or features? Feel free to open an issue or pull request any time. You can also tweet me at [@mplewis](http://twitter.com/mplewis) or email me at [matt@mplewis.com](mailto:matt@mplewis.com).

# License

Copyright (c) 2014 Matthew Lewis. Licensed under [the MIT License](http://opensource.org/licenses/MIT).
