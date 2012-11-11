d3gem
=====

For harnessing those Flawless Square Emeralds

----

`d3gem` is a very simple utility tool for helping with Diablo 3 gem crafting.
What it does is calculating whether you have enough lesser gems to make few greater ones,
and how many you are missing (or will have left).


Installation
------------

Use *pip* to get the ``d3gem`` command in your shell::

    $ pip install d3gem

Or just download the package and run ``d3gem.py`` directly (e.g. with ``python ./d3gem.py``).


Usage
-----

Specify which gem(s) you are trying to make and you will see how many Flawless Square ones
you will need for that::

    $ d3gem 1fst
    You DON'T have enough lesser gems to make 1 Flawless Star gem(s).
    The equivalent of 81 Flawless Square gem(s) is missing for that.

You can also say gems what you already have in *stock*, so that you'll see how many
you are still missing to perform your craft::

    $ d3gem 1fst -s 20fsq,1rsq,1st
    You DON'T have enough lesser gems to make 1 Flawless Star gem(s).
    The equivalent of 25 Flawless Square gem(s) is missing for that.

or, alternatively, how many you'll have left::

    $ d3gem 1st -s 20fsq,1rsq
    You DO have enough lesser gems to make 1 Star gem(s).
    Afterwards you will still have the equivalent of 2 Flawless Square gem(s).

Type ``d3gem --help`` to get the list of gem class abbrevations.


TODOs
-----

* Show missing/excess gems converted to better classes than just Flawless Squares
* Make target gems optional and show what's the highest gem you can craft with given stock
  and how many more you need for even higher class
* Maybe store stock in config file?...

Suggestions and pull requests welcome :)
