# -*- coding: utf-8 -*-
#
# generic tools for apps
#


def format_float(number):                                       # {{{
    """
    format the display style of a float number
    """
    threshold_min = 0.001
    threshold_max = 9999.9
    fix_fmt = '{:,.1f}'    # comma as a thousands separator
    exp_fmt = '{:.1e}'
    #
    if isinstance(number, int) or isinstance(number, float):
        #return type(number)
        pass
    else:
        return False
    #
    if (number > threshold_max) or (number < threshold_min):
        str = exp_fmt.format(number)
    else:
        str = fix_fmt.format(number)
    #
    return str
# }}}


