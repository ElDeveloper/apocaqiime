#!/usr/bin/env python
# File created on 06 Aug 2013
from __future__ import division

from collections import defaultdict
from cogent.parse.fasta import MinimalFastaParser
from qiime.util import parse_command_line_parameters, make_option

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.7.0"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Release"


script_info = {}
script_info['brief_description'] = "Re-tag sequence identifiers"
script_info['script_description'] = "Re-label sequence identifiers in a QIIME"+\
    "  compliant format, i. e. the first set of characters is the sample "+\
    "identifier suffixed with a number."
script_info['script_usage'] = [("Rename each of the sequence identifiers for "
    "use with QIIME","Have each sequence identifier re-labeled by the first "
    "set of characters in the sequence id plus an index","%prog -i seqs.fasta "
    "-o relabeled.fasta")]
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-f','--input_fasta',type="existing_filepath",help='the input '
    'filepath to the FAST formatted file')
]
script_info['optional_options'] = [
    make_option('-o','--output_fasta',type="new_dirpath",help='the output '
    'filepath [default: %default]', default='fixed_file.fasta'),
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    input_fasta = opts.input_fasta
    output_fasta = opts.output_fasta

    fd_out = open(output_fasta, 'w')

    seqs_dict = defaultdict(int)

    for sequence_id, sequence in MinimalFastaParser(open(input_fasta)):
        key = sequence_id.split(' ')[0]

        fd_out.write('>%s_%d %s\n' % (key, seqs_dict[key], sequence_id))
        fd_out.write(sequence+'\n')

        seqs_dict[key] += 1

    fd_out.close()

if __name__ == "__main__":
    main()