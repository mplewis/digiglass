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

# Troubleshooting

Having issues? Try clearing the app's cache: `digiglass --clear-cache`

# Contributions

Bug reports, fixes, or features? Feel free to open an issue or pull request any time. You can also tweet me at [@mplewis](http://twitter.com/mplewis) or email me at [matt@mplewis.com](mailto:matt@mplewis.com).

# License

Copyright (c) 2014 Matthew Lewis. Licensed under [the MIT License](http://opensource.org/licenses/MIT).
