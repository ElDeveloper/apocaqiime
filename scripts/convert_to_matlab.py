#!/usr/bin/env python
# File created on 12 Feb 2013
from __future__ import division

__author__ = "Yoshiki Vazquez-Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez-Baeza"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Yoshiki Vazquez-Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from qiime.parse import parse_mapping_file
from apocaqiime.parse import parse_smp_unifrac_distances
from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-i','--input_fp',type="existing_filepath",help='file with '
        'a list unifrac distances associated with a PersonalID and a time '
        'point'),
#    make_option('-m','--mapping_fp',type="existing_filepath",help='metadata '
#        'mapping file with the PersonalIDs')
    make_option('-s','--site_id',type="string",help='name of the metadata'
        'mapping file column header point', default='forhead')
]
script_info['optional_options'] = [
    make_option('-o','--output_prefix',type="string",help='the output of the'
        'script, two tab separated value formatted files one with the a unique '
        'identifier per line and the other with each time point as a column and'
        ' and each line corresponding to the unique identifier '
        ' [default: %default]', default="SMP_processes_file")
]
script_info['version'] = __version__


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    input_fp = opts.input_fp
#    mapping_fp = opts.mapping_fp
    output_prefix = opts.output_prefix
    column_name = opts.site_id

#    data, headers, _ = parse_mapping_file(open(mapping_fp, 'U'))

    lines = open(input_fp, 'U').readlines()

    individuals, time_points, data = parse_smp_unifrac_distances(lines)

    # write the three output files
    fd = open(output_prefix+'individuals.txt', 'w')
    fd.writelines([ind+'.'+column_name+'\n' for ind in individuals])
    fd.close

    fd = open(output_prefix+'time_points.txt', 'w')
    fd.writelines('\t'.join(map(str, time_points)))
    fd.close()

    # the data goes tab separated
    fd = open(output_prefix+'data.txt', 'w')
    fd.writelines(['\t'.join(map(str, element))+'\n' for element in data])
    fd.close()

if __name__ == "__main__":
    main()