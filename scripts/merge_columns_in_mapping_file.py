#!/usr/bin/env python
# File created on 07 May 2013
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
script_info['brief_description'] = "Merge columns in a metadata mapping file"
script_info['script_description'] = "Use at your own risk"
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-m', '--mapping_fp', type="existing_filepath", help='the input'
    ' filepath of the metadata mapping file.'),
    make_option('-c', '--columns_to_merge', help='Columns separated by two '
    'ampersands (&&) that will get merged', action='append', default=None)]
script_info['optional_options'] = [
    make_option('-o', '--output_fp', type="new_filepath", help="the name of the"
    " mapping file with the merged columns [default: %default]", default=
    "merged_columns_mapping_file.txt")]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    columns_to_merge = opts.columns_to_merge
    mapping_fp = opts.mapping_fp
    output_fp = opts.output_fp

    try:
        data, headers, comments = parse_mapping_file(open(mapping_fp, 'U'))
    except:
        option_parser.error('Bro, that doesn\'t look like a mapping file')

    for merging in columns_to_merge:
        retrieve = lambda x: headers.index(x)
        indices = map(retrieve, merging.split('&&'))

        headers.append(''.join([headers[element] for element in indices]))

        for line in data:
            line.append(''.join([line[element] for element in indices]))

    # this should never happen
    assert len(headers) == len(data[0]), "Something went horribly wrong, "+\
        "that's what you get for using non-unit-tested software"

    lines = format_mapping_file(headers, data, comments)

    fd = open(output_fp, 'w')
    fd.writelines(lines)
    fd.close()

if __name__ == "__main__":
    main()