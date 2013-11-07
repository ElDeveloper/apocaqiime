#!/usr/bin/env python
# File created on 05 Jul 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Use at your own risk"


from apocaqiime.distance_matrix import ratios_for_category
from numpy import argmin, eye
from qiime.parse import parse_distmat, parse_mapping_file
from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [\
 # Example required option
    make_option('-i','--matrix_fp',type="existing_filepath",help='the input '
    'distance matrix'),
    make_option('-m','--mapping_fp',type="existing_filepath",help='the input '
    'file path of the mapping file'),
    make_option('-s','--subject',type="string",help='the input '
    'name of the category that separates the samples by subject')
    # make_option('-g','--gradient',type="string",help='the input '
    # 'file path of the mapping file')

]
script_info['optional_options'] = [\
 # Example optional option
    make_option('-o','--output_fp',type="new_filepath",help='the output '
    'file path with stuff [default: %default]', default='sacagawea.txt')
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    subject_header_name = opts.subject
    # gradient_header_name = opts.gradient
    matrix_fp = opts.matrix_fp
    mapping_fp = opts.mapping_fp

    matrix_header, matrix_data = parse_distmat(open(matrix_fp, 'U'))
    mapping_data, mapping_headers, _ = parse_mapping_file(open(mapping_fp, 'U'))

    out_dict = ratios_for_category(matrix_header, matrix_data, mapping_headers, mapping_data, subject_header_name)

    print 'Subject\tPercent'
    for key, value in out_dict.iteritems():
        print '%s\t%f' % (key, (value[0]/value[1])*100)

if __name__ == "__main__":
    main()
