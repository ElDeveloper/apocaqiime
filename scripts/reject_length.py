#!/usr/bin/env python
# File created on 09 Aug 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza", "William David Winter Van Treuren The Third"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Use at your own risk"


from cogent.parse.fasta import MinimalFastaParser
from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    # Example required option
    make_option('-f','--fasta_fp',type="existing_filepath",help='the input '
    'FASTA file'),
    make_option('--length',type="int",help='the minimum length a sequence '
    'should have to be retained')]

script_info['optional_options'] = [
    # Example optional option
    make_option('-o','--output_fasta_fp',type="new_filepath",help='the output '
    'directory [default: %default]'),
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    fasta_fp = opts.fasta_fp
    output_fp = opts.output_fasta_fp
    minimum_length = opts.length

    fd_out = open(output_fp, 'w')

    for seq_id, seq in MinimalFastaParser(open(fasta_fp, 'U')):
        if len(seq) < minimum_length:
            continue

        fd_out.write('>'+seq_id+'\n')
        fd_out.write(seq+'\n')

    fd_out.close()


if __name__ == "__main__":
    main()