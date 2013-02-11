#!/usr/bin/env python
# File created on 06 Feb 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from qiime.parse import parse_coords
from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-i','--input_fp',type="existing_filepath",help='coords file'),
    make_option('-o','--output_fp',type="new_filepath",help='new file for use '
        'with Mathematica and the awesome program that created this video '
        'http://www.youtube.com/watch?v=Pb272zsixSQ')
]
script_info['optional_options'] = [
    make_option('-n','--number_of_dimensions',type="int",help='number of '
        'dimensions to use from the coordinates file [default= %default]',
        default=3),\
]
script_info['version'] = __version__



def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    input_fp = opts.input_fp
    output_fp = opts.output_fp
    dimensions = opts.number_of_dimensions

    _, coords, _, _ = parse_coords(open(input_fp, 'U'))

    fd = open(output_fp, 'w')
    for line in coords:
        fd.write('\t'.join(map(str, line[:dimensions])))
        fd.write('\n')
    fd.close()

if __name__ == "__main__":
    main()