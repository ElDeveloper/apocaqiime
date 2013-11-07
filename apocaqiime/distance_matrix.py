#!/usr/bin/env python
# File created on 08 Jul 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.7.0"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Use at your own risk"

from numpy import eye, argmin, min

def ratios_for_category(matrix_header, matrix_data, mapping_headers, mapping_data, subject_header_name):
    """ """
    subject_header_index = mapping_headers.index(subject_header_name)
    subject_names = list(set([line[subject_header_index]
        for line in mapping_data]))

    number = 0
    out_dict = {}

    comparison_matrix = (eye(len(matrix_header))*10)+matrix_data

    for subject in subject_names:
        sample_ids_list = [line[0] for line in mapping_data if line[subject_header_index] == subject]

        print 'Subject ', '"'+subject+'"', ', with sample identifiers %s.' % ', '.join(sample_ids_list)

        for sample_id in sample_ids_list:
            row_index = matrix_header.index(sample_id)

            the_minimum = matrix_header[argmin(comparison_matrix[row_index])]
            print 'Closest sample to: "', sample_id, '" is: "', the_minimum, '" ',str(min(comparison_matrix[row_index]))
            if the_minimum in sample_ids_list:
                number=number+1

        # should never happen but if ithappens then well ... :/
        assert number<=len(sample_ids_list), "The number of similarities "+\
            "cannot be greater than the number of samples. The distance "+\
            "matrix must be really really screwed up."

        out_dict[subject] = (number, len(sample_ids_list))

        number = 0

    return out_dict