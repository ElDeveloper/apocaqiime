#!/usr/bin/env python
# File created on 04 Oct 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.7.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from os import listdir, makedirs
from os.path import join
from re import compile, search, findall, escape
from qiime.util import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    # Example required option
    make_option('-i','--input_dir',type="existing_dirpath",help='the input filepath'),
    make_option('--prefix',type="string",help='the prefix to look for the files'),
    make_option('-o','--output_dir',type="new_dirpath",help='the output directory [default: %default]'),
]
script_info['optional_options'] = [
 # Example optional option
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    input_directory = opts.input_dir
    file_prefix = opts.prefix
    output_directory = opts.output_dir

    all_the_files = [element for element in listdir(input_directory) if element.startswith(file_prefix)]
    global_file_path = file_prefix + '_GLOBAL.txt'

    if not len(all_the_files):
        option_parser.error("no files were found")

    if global_file_path not in all_the_files:
        option_parser.error("cannot continue ... no global file found")

    try:
        makedirs(output_directory)
    except:
        pass

    fd = open(join(input_directory, global_file_path), 'U')
    global_file_contents = ''.join(fd.readlines())
    fd.close()


    for element in all_the_files:
        if element == global_file_path:
            continue

        sample_id = element.replace(file_prefix+'_', '').replace('_huge', '')
        escaped_sample_id = escape(sample_id)

        # style="fill: rgb(0,0,73); fill-opacity: 1"
        # re = compile('\\<path\ id\=\"'+escaped_sample_id+'\"\ d\=\\"M\\ ([A-Za-z0-9\\.\\ \\-\\,]+)\\" style\\=\\"(.*)\\"\\>\\<\\/path\\>')
        re = compile('\\<path\ id\=\"'+escaped_sample_id+'\"\ d\=\\"M\\ ([A-Za-z0-9\\.\\ \\-\\,]+)\\" style\\=\\"([A-Za-z0-9\\.\\ \\-\\,\\(\\)\\:\\;]+)\\"\\>\\<\\/path\\>')

        fd = open(join(input_directory, element), 'U')
        per_sample_file = ''.join(fd.readlines())
        fd.close()

        big_sphere_contents = findall(re, per_sample_file)
        small_sphere_contents = findall(re, global_file_contents)

        if big_sphere_contents == None or small_sphere_contents == None:
            print 'Problem found with %s, skipping it for now' % sample_id
            continue

        temp = global_file_contents

        matchable = '<path id="%s"' % sample_id
        matchable = matchable + ' d="M %s" style="%s"></path>'

        print matchable

        for index in range(0, min([len(small_sphere_contents), len(big_sphere_contents)])):
            # print matchable % small_sphere_contents[index], matchable % big_sphere_contents[index]
            temp = temp.replace(matchable % small_sphere_contents[index], matchable % big_sphere_contents[index])

        # print sample

        print len(small_sphere_contents)
        print len(big_sphere_contents)

        # continue

        fd_out = open(join(output_directory, element+'.svg'), 'w')
        fd_out.write(temp)
        fd_out.close()



if __name__ == "__main__":
    main()