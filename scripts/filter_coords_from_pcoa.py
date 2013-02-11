#!/usr/bin/env python
# File created on 05 Feb 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from qiime.format import format_coords
from qiime.parse import parse_coords, parse_mapping_file
from qiime.filter import sample_ids_from_metadata_description
from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-i','--input_coords',type="existing_filepath",help='input file'
        ' of coordinates'),
]
script_info['optional_options'] = [
    # Example optional option
    make_option('-m','--mapping_fp',type="existing_filepath", help='mapping '
        'file corresponding to the coords file', default=None),
    make_option('-o','--output_fp',type="new_filepath",help='the output '
        'directory with all the coordinate files resulting of the filtering '
        '[default: %default]', default='filtered_pc.txt'),
    make_option('-s','--valid_states',type='string',help='string containing '
        'valid states, e.g. "STUDY_NAME:DOB"', default=None),
    make_option('--negate',default=False, action='store_true', help='discard '
        'specified samples (instead of keeping them) [default: %default]")]'),
    make_option('--mapping_header_name',type='string',help='string containing '
        'the name of the column in the metadata mapping field to sort the '
        'coordinates', default=None)
]
script_info['version'] = __version__



def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    coords_fp = opts.input_coords
    mapping_fp = opts.mapping_fp
    output_fp = opts.output_fp
    valid_states = opts.valid_states
    negate = opts.negate
    mapping_header_name = opts.mapping_header_name

    coords_ids, coords, eigen_values, pct_exp = parse_coords(open(coords_fp,
        'U'))

    data, headers, _ = parse_mapping_file(open(mapping_fp, 'U'))

    if mapping_fp and valid_states:
        valid_sample_ids = sample_ids_from_metadata_description(
            open(mapping_fp, 'U'), valid_states)

    valid_coords_ids, valid_coords = filter_sample_ids_from_coords(coords_ids,
        coords, valid_sample_ids, negate)

    if mapping_header_name:
        sorted_sample_ids = sort_sample_ids(data, headers, mapping_header_name)
        sorted_coord_ids, sorted_coords = sort_coords(valid_coords_ids,
            valid_coords, sorted_sample_ids)
        valid_coords_ids, valid_coords = sorted_coord_ids, sorted_coords

    lines = format_coords(valid_coords_ids, valid_coords, eigen_values, pct_exp)
    fd = open(output_fp, 'w')
    fd.writelines(lines)
    fd.close

def filter_sample_ids_from_coords(coords_ids, coords, valid_sample_ids,
        negate=False):
    """ """
    out_coord_ids, out_coords = [], []

    if negate:
        def keep_sample(s):
            return s not in valid_sample_ids
    else:
        def keep_sample(s):
            return s in valid_sample_ids

    for sample_id, coord in zip(coords_ids, coords):
        if keep_sample(sample_id):
            out_coord_ids.append(sample_id)
            out_coords.append(coord)

    return out_coord_ids, out_coords

def sort_sample_ids(data, headers, header_name):
    """ """
    interesting_index = headers.index(header_name)

    print 'The interesting index is %s ' % interesting_index
    sort_lambda = lambda x: float(x[interesting_index])

    sorted_mapping_data = sorted(data, key=sort_lambda)

    # for element in sorted_mapping_data:
    #     print 'element %s' % element[0]

    return [line[0] for line in sorted_mapping_data]

def sort_coords(coords_ids, coords, sorted_ids):
    """ """
    sorted_coords, sorted_sids = [], []

    for single_id in sorted_ids:
        try:
            lost_index = coords_ids.index(single_id)
        except ValueError:
            continue
        sorted_coords.append(coords[lost_index])
        sorted_sids.append(single_id)

    return sorted_sids, sorted_coords

if __name__ == "__main__":
    main()