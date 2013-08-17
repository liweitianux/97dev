# -*- coding: utf-8 -*-

"""
tools for haystack search
"""

from haystack.query import SearchQuerySet

import itertools


def objects_of_sqs(sqs):
    """
    return the corresponding model set of the SearchQuerySet
    """
    if isinstance(sqs, SearchQuerySet):
        return itertools.imap(lambda x: x.object, sqs)
    else:
        return sqs

def limit(seq, count=None):
    """
    return the first 'count' items in 'seq'
    if 'count=None', then all items returned
    """
    return itertools.islice(seq, count)


