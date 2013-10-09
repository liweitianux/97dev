# -*- coding: utf-8 -*-
#
# tools for apps/recommend
#

from django.db.models import Count

from recommend import models as rm

import re


def make_tag(ids=[], tag='tag', sep='_'):                       # {{{
    """
    make tag by using given list of ids

    if 'ids' is a list of integers, then sort them by magnitude
    """
    if isinstance(ids, tuple):
        ids = list(ids)
    # check list element type
    all_ints = all(isinstance(item, int) for item in ids)
    if all_ints:
        # sort ints by magnitude
        ids.sort()
    #
    tag_name = tag
    for id in ids:
        tag_name = '%s%s%s' % (tag_name, sep, id)
    return tag_name
# }}}


def get_research_config(atoms=[]):                              # {{{
    """
    return the found ResearchConfig object
    by filtering on the given atoms list
    """
    if not atoms:
        return False
    # convert id list to obj list
    if isinstance(atoms[0], int):
        atoms = [rm.ResearchAtom.objects.get(id=id) for id in atoms]
    qs = rm.ResearchConfig.objects.annotate(c=Count('researchAtoms'))\
            .filter(c=len(atoms))
    for atom in atoms:
        qs = qs.filter(researchAtoms=atom)
    if not qs:
        return None
    elif len(qs) == 1:
        return qs[0]
    else:
        return False
# }}}


def make_config_display(atoms=[]):                              # {{{
    """
    make a display string for the given config
    """
    disp_str = u''
    if not atoms:
        return disp_str
    # convert to list
    if isinstance(atoms, tuple):
        atoms = list(atoms)
    # check list element type
    all_ints = all(isinstance(item, int) for item in atoms)
    if all_ints:
        # sort ints by magnitude and convert to objects list
        atoms.sort()
        atoms = [rm.ResearchAtom.objects.get(id=id) for id in atoms]
    #
    for atom in atoms:
        disp_str = '%s%s | ' % (disp_str, atom.display())
    disp_str = re.sub(r'(^\s*\|\s*)|(\s*\|\s*$)', '', disp_str)
    #
    return disp_str
# }}}


