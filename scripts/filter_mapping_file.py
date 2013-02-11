#!/usr/bin/env python
# File created on 05 Feb 2013
from __future__ import division

__author__ = "AUTHOR_NAME"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["AUTHOR_NAME"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "AUTHOR_NAME"
__email__ = "AUTHOR_EMAIL"
__status__ = "Development"

from qiime.parse import parse_mapping_file
from qiime.format import format_mapping_file
from qiime.filter import sample_ids_from_metadata_description
from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [\
 # Example required option
    make_option('-m','--input_fp',type="existing_filepath",help='mapping file'),
    make_option('-s','--valid_states',type='string',help='string containing '
        'valid states, e.g. "STUDY_NAME:DOB"', default=None),
]
script_info['optional_options'] = [\
    make_option('-o','--output_fp',type="new_filepath",help='output file'),\
]
script_info['version'] = __version__



def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    mapping_fp = opts.input_fp
    out_mapping_fp = opts.output_fp
    valid_states = opts.valid_states

    if mapping_fp and valid_states:
        valid_sample_ids = sample_ids_from_metadata_description(
            open(mapping_fp, 'U'), valid_states)

    data, headers, _ = parse_mapping_file(open(mapping_fp, 'U'))

    good_mapping_file = []
    for line in data:
        if line[0] in valid_sample_ids:
            good_mapping_file.append(line)

    lines = format_mapping_file(headers, good_mapping_file)

    fd = open(out_mapping_fp, 'w')
    fd.write(lines)
    fd.close()

if __name__ == "__main__":
    main()