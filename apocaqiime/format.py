from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


# This function was directly ported from QIIME 1.8.0, tests and other
# information can be found there.
# https://github.com/biocore/qiime/blob/d4333e2ea06af942f1f61148c4ccb02ffc438d6b/qiime/format.py
def format_coords(coord_header, coords, eigvals, pct_var, headers = True):
    """formats coords given specified coords matrix etc."""
    result = []
    if (headers):
        result.append('pc vector number\t' +
           '\t'.join(map(str, range(1,len(coords[0])+1))))
        for name, row in zip(coord_header, coords):
            result.append('\t'.join([name] + map(str, row)))
        result.append('')
        result.append('')
        result.append('eigvals\t' + '\t'.join(map(str,eigvals)))
        result.append('% variation explained\t' +
           '\t'.join(map(str, pct_var)))
    else:
        result = ['\t'.join(map(str, row)) for row in coords]
        result.append('')
    return '\n'.join(result)
