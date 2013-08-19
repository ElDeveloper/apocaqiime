#!/usr/bin/env python
# File created on 19 Aug 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from copy import deepcopy
from operator import add, sub, mul, truediv, pow

OPERATION_FUNCTIONS = {'+':add, '-':sub, '*':mul, '/':truediv, '**':pow}

def apply_operation_on_mapping_file_columns(headers, data, categories, titles,
                                            operation='+'):
    """ """
    assert operation in ['+', '-', '*', '/', '**'], "Operation not allowed"

    out_headers = deepcopy(headers)
    out_data = deepcopy(data)

    # for j in range(0,len(categories)):
    #     out_headers.append(titles[j])
    for i, group_of_categories in enumerate(categories):
        out_headers.append(titles[i])
        for j, line in enumerate(out_data):
            temp = 0.0
            indices = map(lambda x: out_headers.index(x), group_of_categories.split(','))

            for index in indices:
                # exec 'temp = temp %s float(line[index])' % operation
                # lookup the value in the dictionary
                temp = OPERATION_FUNCTIONS[operation](temp, float(line[index]))

            out_data[j].append('%f' % temp)

    return out_headers, out_data
