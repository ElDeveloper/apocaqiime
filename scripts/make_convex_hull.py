#!/usr/bin/env python
# File created on 09 Jul 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.7.0"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Use at your own risk"

# the creation of the convex hull is based on the example as provided by scipy
# see this URL http://docs.scipy.org/doc/scipy-dev/reference/generated/scipy.spatial.ConvexHull.html
from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.pyplot as plt
from qiime.sort import natsort
from qiime.parse import parse_coords, parse_mapping_file
from qiime.util import (parse_command_line_parameters, make_option,
    qiime_system_call)
from qiime.colors import get_qiime_hex_string_color
from os.path import splitext
from qiime.plot_taxa_summary import make_legend

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-i','--coordinates_fp', type="existing_filepath",help='the '
    'input coordinates filepath'),
    make_option('-m','--mapping_file_fp', type="existing_filepath",help='the '
    'mapping file filepath'),
    make_option('-c','--category',type="string",help='header name of the '
    'category of interest that you want the convex hulls to be created on')
]
script_info['optional_options'] = [
    make_option('-j','--chuck_norris_joke', action="store_true", help='if set'
    'a random chuck norris joke will be printed to screen', default=False),
    make_option('-o','--output_fp', type="new_filepath", help='filename and '
    'format for the plot, the extension will determine the format of the '
    'output file (pdf, eps or png)', default='convex_hull.png')
]
script_info['version'] = __version__

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    chuck_norris_joke = opts.chuck_norris_joke
    coordinates_fp = opts.coordinates_fp
    mapping_file_fp = opts.mapping_file_fp
    category_header_name = opts.category
    output_fp = opts.output_fp

    # have a swell day Yoshiki from the future 
    if chuck_norris_joke:
        o, e, _ = qiime_system_call('curl http://api.icndb.com/jokes/random')

        exec 'joke = %s' % o.strip()
        print joke['value']['joke']
        exit(0)

    coords_headers, coords_data, coords_eigenvalues, coords_percents =\
        parse_coords(open(coordinates_fp, 'U'))
    mapping_data, mapping_headers, _ = parse_mapping_file(open(mapping_file_fp, 'U'))

    category_header_index = mapping_headers.index(category_header_name)
    category_names = list(set([line[category_header_index]
        for line in mapping_data]))


    main_figure = plt.figure()
    main_axes = main_figure.add_subplot(1, 1, 1, axisbg='black')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    main_axes.tick_params(axis='y', colors='none')
    main_axes.tick_params(axis='x', colors='none')
 

    # sort the data!!! that way you can match make_3d_plots.py
    sorted_categories = natsort(category_names)
    colors_used = []

    for index, category in enumerate(sorted_categories):
        sample_ids_list = [line[0] for line in mapping_data if line[category_header_index] == category]

        qiime_color = get_qiime_hex_string_color(index)

        if len(sample_ids_list) < 3:
            continue

        colors_used.append(qiime_color)

        indices = [coords_headers.index(sample_id) for sample_id in sample_ids_list]
        points = coords_data[indices, :2]# * coords_percents[:2]

        hull = ConvexHull(points)
        main_axes.plot(points[:,0], points[:,1], 'o', color=qiime_color)
        for simplex in hull.simplices:
            main_axes.plot(points[simplex,0], points[simplex,1], 'w-')
        main_axes.plot(points[hull.vertices,0], points[hull.vertices,1], '--', lw=2, color=qiime_color)
        # plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], '--', color=qiime_color)
    # plt.show()

    main_figure.savefig(output_fp)

    name = splitext(output_fp)[0]
    extension = splitext(output_fp)[1].replace('.', '')

    make_legend(sorted_categories, colors_used, 0, 0, 'black', 'white', name,
                extension, 80)

if __name__ == "__main__":
    main()