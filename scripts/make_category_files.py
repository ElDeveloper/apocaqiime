#!/usr/bin/env python
# File created on 24 Apr 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from os.path import join
from cogent.util.misc import makedirs
from qiime.parse import parse_mapping_file
from qiime.filter import (sample_ids_from_metadata_description,
    filter_mapping_file)
from qiime.util import parse_command_line_parameters, make_option
from qiime.util import MetadataMap

script_info = {}
script_info['brief_description'] = "Use at your own risk"
script_info['script_description'] = "Use at your own risk"
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-m','--mapping_fp',type="existing_filepath",help='mapping file'
    'in a QIIME compliant format'),
    make_option('-a','--coloring_header_name',type="string",help='header in the'
    ' mapping file to separate the subjects by'),
    make_option('-s','--subject_header_name',type="string",help='header in the'
    ' mapping file to create individual files')
]
script_info['optional_options'] = [
    make_option('-o','--output_path',type="new_path", help='path where all'
    'category files will be stored [default=colord_by_COLRING_HEADER_NAME_sepa'
    'rated_by_SUBJECT_HEADER_NAME]', default=None),
    make_option('-f', '--force', action='store_true', dest='force', help='Force'
    ' overwrite of existing output directory (note: existing files in '
    'output_dir will not be removed) [default: %default]')
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    mapping_fp = opts.mapping_fp
    coloring_header_name = opts.coloring_header_name
    subject_header_name = opts.subject_header_name
    force = opts.force

    if opts.output_path == None:
        output_path = 'colored_by_%s_separated_by_%s' % (coloring_header_name,
            subject_header_name)
    else:
        output_path = opts.output_path

    try:
        makedirs(output_path)
    except:
        if not force:
            option_parser.error('Pfft something bad happened when creating the '
                'output directory, try a different --output_path.')

    data, headers, _ = parse_mapping_file(open(mapping_fp, 'U'))

    subject_index = headers.index(subject_header_name)
    coloring_index = headers.index(coloring_header_name)

    coloring_values = list(set([row[coloring_index] for row in data]))

    for c_value in coloring_values:
        sample_ids = sample_ids_from_metadata_description(open(mapping_fp, 'U'),
            '%s:%s' % (coloring_header_name, c_value))

        _headers, _data = filter_mapping_file(data, headers, sample_ids, True)
        # print _headers
        # print 'The length is %d and %d' % (len(_data), len(_data[0]))
        # print 'This is subject index %d' % subject_index
        per_color_subject_values = list(set([row[subject_index] for row in _data]))

        fd = open(join(output_path, c_value+'.txt'), 'w')
        for s in per_color_subject_values:
            fd.write('%s\n' % s)
        fd.close()


if __name__ == "__main__":
    main()
