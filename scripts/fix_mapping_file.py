#!/usr/bin/env python
# File created on 08 Mar 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from qiime.util import qiime_system_call, get_qiime_temp_dir
from qiime.format import format_mapping_file
from qiime.parse import parse_mapping_file
from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = "Make the mapping file something unix friendly"
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [\
    make_option('-i','--input_fp',type="existing_filepath",help='the input filepath')
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    try:
        data, headers, comments = parse_mapping_file(open(opts.input_fp, 'U'))
    except:
        option_parser.error('That doesn\'t look like a mapping file')

    lines = format_mapping_file(headers, data, comments)

    fd = open(opts.input_fp, 'w')
    fd.writelines(lines)
    fd.close()

if __name__ == "__main__":
    main()