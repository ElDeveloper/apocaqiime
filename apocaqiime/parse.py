#!/usr/bin/env python
# File created on 12 Feb 2013
from __future__ import division

__author__ = "Yoshiki Vazquez-Baeza"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Yoshiki Vazquez-Baeza"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Yoshiki Vazquez-Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from numpy import zeros
from qiime.sort import natsort

def parse_smp_unifrac_distances(lines):
    """ """
    header = lines[0]
    data = lines[1::]

    unique_personal_ids = natsort(list(set([line.split('\t')[0] for line in data])))
    unique_time_points = list(set([line.split('\t')[1] for line in data]))

    # sort the time-points
    unique_time_points = sorted(unique_time_points, key=lambda x:float(x))

    _matrix = [line.split('\t') for line in data]

    output_data = zeros([len(unique_personal_ids), len(unique_time_points)])
    for index, person_id in enumerate(unique_personal_ids):
        sub_matrix = [row for row in _matrix if row[0] == person_id]

        # sort by time point submatrix
        sub_matrix = sorted(sub_matrix, key=lambda x: float(x[1]))

        for element in sub_matrix:
            per_value_index = unique_time_points.index(element[1])
            output_data[index][per_value_index] = float(element[2])

    return unique_personal_ids, unique_time_points, output_data