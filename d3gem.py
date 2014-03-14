#!/usr/bin/env python
"""
d3gem -- For helping with Diablo 3 gem madness

:author: Karol Kuczmarski "Xion"
:license: GNU General Public License Version 3 (see LICENSE file)
"""
__version__ = "0.2.1"
__description__ = "Diablo 3 gem crafting helper"
__author__ = 'Karol Kuczmarski "Xion"'
__license__ = "GPLv3"


import argparse
import numbers
import os
import re


def main():
    """Entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()

    # parse the target gem class and quantity
    target = parse_gem_cluster(args.target)
    if len(target) > 1:
        print "Sorry, you can only specify one class of target gems."
        exit(1)
    target_class_name = gem_class_name(next(target.iterkeys()))
    target_quantity = next(target.itervalues())

    stock = parse_gem_cluster(args.stock)

    # convert everything to basic gems and compare quantities
    target_basic = to_basic_gems(target)
    stock_basic = to_basic_gems(stock)
    if target_basic == stock_basic:
        print "You have just enough lesser gems to make %s %s gem(s)." % (
            target_quantity, target_class_name)
    elif target_basic < stock_basic:
        residue = stock_basic - target_basic
        print "You DO have enough lesser gems to make %s %s gem(s)." % (
            target_quantity, target_class_name)
        print "Afterwards, you will still have the equivalent of:"
        print_gems(residue, verbose=args.verbose)
    else:  # target_basic > stock_basic
        missing = target_basic - stock_basic
        print "You DON'T have enough lesser gems to make %s %s gem(s)." % (
            target_quantity, target_class_name)
        print "What is missing is the equivalent of:"
        print_gems(missing, verbose=args.verbose)


def print_gems(gems, verbose=False):
    """Prints the quantity of gems in user-friendly format,
    using various representations with different 'best' gem classes
    for comparison.
    """
    if verbose:
        gem_clusters = to_various_representations(gems)
        separator = " or "
        print " " * len(separator) + format_gem_clusters(
            gem_clusters, sep=os.linesep + separator)
    else:
        _, basic_class_name = GEM_CLASSES[0]
        print "%s %s gem(s)" % (gems, basic_class_name)


# Gem basics

GEM_CLASSES = [
    ('fsq', "Flawless Square"),
    ('psq', "Perfect Square"),
    ('rsq', "Radiant Square"),
    ('st', "Star"),
    ('fst', "Flawless Star"),
    ('pst', "Perfect Star"),
    ('rst', "Radiant Star"),
    ('mq', "Marquise"),
]

GEMS_PER_CRAFT = 3


def gem_class_name(ident):
    """Gets the name of gem class given its identifier."""
    return next(name for class_, name in GEM_CLASSES if class_ == ident)


def gem_class_order(ident):
    """Gets the order (index) of gem class given its identifier.
    Basic gems are of class 0.
    """
    return next(i for i, (c, _) in enumerate(GEM_CLASSES) if c == ident)


# Gem arithmetic

def to_basic_gems(cluster):
    """Returns a number of basic gems needed for given gem cluster.
    :param cluster: Gem cluster (a dict)
    """
    return sum(quantity * GEMS_PER_CRAFT ** gem_class_order(class_)
               for class_, quantity in cluster.iteritems())


def to_best_possible_gems(gems, best=None):
    """Returns a gem cluster with best possible gems for given ones.
    :param gems: Gem cluster (a dict) or number of basic gems (an int)
    :param best: What gem class is considered best
    """
    if not isinstance(gems, numbers.Integral):
        gems = to_basic_gems(gems)

    best = best or len(GEM_CLASSES) - 1
    if not isinstance(best, (int, long)):
        best = gem_class_order(best)

    cluster = {}
    for order in reversed(xrange(best + 1)):
        count = GEMS_PER_CRAFT ** order
        if gems >= count:
            class_, _ = GEM_CLASSES[order]
            cluster[class_] = gems / count
            gems %= count

    return cluster


def to_various_representations(gems):
    """Returns a list of various gem clusters equivalent to given one.

    The clusters returned differ in what they consider the 'best' gem,
    so that user can get a better idea of gem quantities.

    :param gems: Gem cluster (a dict) or number of basic gems (an int)
    """
    res = []
    for class_, _ in GEM_CLASSES:
        cluster = to_best_possible_gems(gems, best=class_)
        if cluster.get(class_, 0) == 0:
            break
        res.append(cluster)

    res.reverse()
    return res


# Gem input/output

def parse_gem_cluster(gems):
    """Parses the string or list representation of 'gem cluster'
    into a dictionary that maps gem classes into quantities.
    :param gems: Comma-separated string or list thereof
    """
    if isinstance(gems, basestring):
        gems = [gems]

    cluster = {}
    for s in gems:
        gemspecs = (gs.strip() for gs in s.split(','))  # ex. 1pst,6fsq
        for gs in gemspecs:
            parsed = parse_gem_spec(gs)
            if parsed:
                class_, quantity = parsed
                total = cluster.setdefault(class_, 0)
                cluster[class_] = total + int(quantity)

    return cluster


def parse_gem_spec(gemspec):
    """Parse the string with single gem spec, i.e. text containing
    the gem class symbol and optional quantity, in either order.
    :return: Tuple (gem_class, quantity)
    """
    def sanitize(class_, quantity):
        if quantity is None:
            quantity = 1
        quantity = int(quantity)
        return class_, quantity

    class_first = re.match(r'(?P<class_>\D+)(?P<quantity>\d+)?', gemspec)
    if class_first:
        return sanitize(**class_first.groupdict())

    quantity_first = re.match(r'(?P<quantity>\d+)?(?P<class_>\D+)', gemspec)
    if quantity_first:
        return sanitize(**quantity_first.groupdict())


def format_gem_clusters(gem_clusters, sep=" or "):
    """Formats a list of equivalent gem clusters in to several lines
    of user-friendly text.
    """
    return sep.join(map(format_gem_cluster, gem_clusters))


def format_gem_cluster(gems):
    """Formats a gem cluster as a single line of user-friendly text."""
    return humanized_join("%s %s" % (gems[class_], name)
                          for class_, name in reversed(GEM_CLASSES)
                          if class_ in gems) + " gem(s)"


# Utility functions

def create_argument_parser():
    """Creates argparse commandline parser."""
    parser = argparse.ArgumentParser(
        description="Tells you how many basic Diablo 3 gems "
                    "you need for an upgraded one",
        epilog=os.linesep.join(["Possible gem classes include:",
                                list_gem_classes()]),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('target', type=str, help="Gem you want to make",
                        metavar="TARGET")
    parser.add_argument('--stock', '-s', type=str, action='append', default=[],
                        help="Gems you have in stock for making TARGET. "
                             "Specify them as comma-separated list, "
                             "e.g. '1fst,27fsq'.")

    parser.add_argument('--verbose', '-v', action='store_true', default=False,
                        help="Output the missing or remaining gems "
                             "conveniently converted to several equivalent "
                             "representations.")

    return parser


def list_gem_classes():
    """Returns a list of gem class names and identifiers
    that can be used in the command line argments for the script.
    """
    return os.linesep.join("\t%s:\t%s" % gs for gs in GEM_CLASSES)


def humanized_join(iterable, sep=", ", last_sep=" and "):
    """Joins given iterable in a 'humanized' way, i.e. with different separator
    between last and second-to-last element (typicaly ' and ').
    """
    seq = list(iterable)
    if len(seq) == 1:
        return str(seq[0])
    return sep.join(seq[:-1]) + last_sep + seq[-1]


if __name__ == '__main__':
    main()
