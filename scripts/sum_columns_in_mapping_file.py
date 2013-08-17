#!/usr/bin/env python
# File created on 14 Aug 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from qiime.parse import parse_mapping_file
from qiime.format import format_mapping_file
from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [\
 # Example required option
    make_option('-m','--input_fp',type="existing_filepath",help='mapping file'),
    make_option('-c','--categories', action='append', type="string", help=
    'category names to summ'),
    make_option('-k','--categories_header_names', action='append', 
    type="string", help='category header names for the resulting sums')

]
script_info['optional_options'] = [
    make_option('-o','--output_fp',type="new_filepath",help='output file',
        default='summed.txt'),
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    mapping_fp = opts.input_fp
    categories = opts.categories
    header_names = opts.categories_header_names
    output_fp = opts.output_fp

    if len(categories) != len(header_names):
        option_parser.error('This shouldnt be happening what are you doing?')

    data, headers, _ = parse_mapping_file(open(mapping_fp, 'U'))

    for j in range(0,len(categories)):
        print 'at category %s ' % header_names[j]
        headers.append(header_names[j])
        for k, line in enumerate(data):
            temp = 0.0
            indices = map(lambda x: headers.index(x), categories[j].split(','))
            for index in indices:
                temp = temp + float(line[index])
            data[k].append('%f' % temp)



    lines = format_mapping_file(headers, data)

    fd = open(output_fp, 'w')
    fd.writelines(lines)
    fd.close()



if __name__ == "__main__":
    main()