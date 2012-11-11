#!/usr/bin/env python
"""
d3gem -- For helping with Diablo 3 gem madness
:author: Karol Kuczmarski "Xion"
"""
import re
import argparse


def main():
    """Entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()

    target = parse_gem_cluster(args.target)
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
        print "Afterwards you will still have the equivalent of %s %s gem(s)." % (
            residue, BASIC_CLASS_NAME)
    else:  # target_basic > stock_basic
        missing = target_basic - stock_basic
        print "You DON'T have enough lesser gems to make %s %s gem(s)." % (
            target_quantity, target_class_name)
        print "The equivalent of %s %s gem(s) is missing for that." % (
            missing, BASIC_CLASS_NAME)


# Gem logic

GEM_CLASSES = [
    ('fsq', "Flawless Square"),
    ('psq', "Perfest Square"),
    ('rsq', "Radiant Square"),
    ('st', "Star"),
    ('fst', "Flawless Star"),
    ('pst', "Perfect Star"),
    ('rst', "Radiant Star"),
]
_, BASIC_CLASS_NAME = GEM_CLASSES[0]

GEMS_PER_CRAFT = 3


def gem_class_name(ident):
    """Gets the name of gem class given its identifier."""
    return next(name for class_, name in GEM_CLASSES if class_ == ident)


def to_basic_gems(cluster):
    """Returns a number of basic gems needed for given gem cluster.
    :param cluster: Gem cluster (a dict)
    """
    res = 0
    for class_, quantity in cluster.iteritems():
        order = next(i for i, (c, _) in enumerate(GEM_CLASSES) if c == class_)
        res += quantity * (GEMS_PER_CRAFT ** order if order > 0 else 1)
    return res


# Utility functions

def create_argument_parser():
    """Creates argparse commandline parser."""
    parser = argparse.ArgumentParser(
        description="Tells you how many basic Diablo 3 gems "
                    "you need for an upgraded one")

    parser.add_argument('target', type=str, help="Gem you want to make",
                        metavar="TARGET")
    parser.add_argument('--stock', '-s', type=str, nargs='*',
                        help="Gems you have in stock for making TARGET")

    return parser


def parse_gem_cluster(gems):
    """Parses the string or list representation of 'gem cluster'
    into a dictionary that maps gem classes into quantities.
    :param gems: Comma-separated string or list thereof
    """
    if isinstance(gems, basestring):
        gems = [gems]

    cluster = {}
    for s in gems:
        gemspecs = [gs.strip() for gs in s.split(',')]  # ex. 1pst,6fsq
        for gs in gemspecs:
            m = re.match(r'(\d+)(\w+)', gs)
            if m:
                quantity, class_ = m.groups()
                total = cluster.setdefault(class_, 0)
                cluster[class_] = total + int(quantity)

    return cluster


if __name__ == '__main__':
    main()
