#!/usr/bin/env python
# File created on 12 Feb 2013
from __future__ import division

__author__ = "Yoshiki Vazquez-Baeza"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Yoshiki Vazquez-Baeza"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Yoshiki Vazquez-Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from numpy import array
from cogent.util.unit_test import TestCase, main
from apocaqiime.parse import parse_smp_unifrac_distances

class TopLevelTests(TestCase):
    
    def setUp(self):
        self.data = FORHEAD_TEST
    
    def tearDown(self):
        pass

    def test_parse_smp_unifrac_distances(self):
        individuals, timepoints, data = parse_smp_unifrac_distances(
            FORHEAD_TEST)

        expected_individuals = ['CUB000', 'CUB003', 'CUB004', 'CUB007']
        expected_timepoints = ['0.5', '1', '2', '3', '4', '5', '6', '7', '8']
        expected_data = DATA_MATRIX

        self.assertEquals(expected_individuals, individuals)
        self.assertEquals(expected_timepoints, timepoints)
        self.assertTrue(all((expected_data == data).tolist()))



FORHEAD_TEST = ['Individual\tWeeksSinceStart\tdistFromPrevious\n',
 'CUB000\t0.5\t0.539584815346\n',
 'CUB000\t1\t0.568188662053\n',
 'CUB000\t2\t0.561277138463\n',
 'CUB000\t3\t0.506575452054\n',
 'CUB000\t5\t0.493363835278\n',
 'CUB000\t6\t0.507126889112\n',
 'CUB000\t7\t0.576220926791\n',
 'CUB000\t8\t0.494494033989\n',
 'CUB003\t0.5\t0.521659687139\n',
 'CUB003\t1\t0.568799458575\n',
 'CUB003\t2\t0.594901005623\n',
 'CUB003\t3\t0.590758979206\n',
 'CUB003\t4\t0.531587671829\n',
 'CUB003\t5\t0.669239308438\n',
 'CUB003\t6\t0.635955675839\n',
 'CUB003\t7\t0.640497989011\n',
 'CUB003\t8\t0.631222633107\n',
 'CUB004\t2\t0.511447299215\n',
 'CUB004\t3\t0.48941172761\n',
 'CUB004\t4\t0.507506276121\n',
 'CUB004\t5\t0.476268332252\n',
 'CUB004\t6\t0.512491470868\n',
 'CUB004\t7\t0.495011849983\n',
 'CUB004\t8\t0.469078786767\n',
 'CUB007\t0.5\t0.626489382526\n',
 'CUB007\t1\t0.579714425673\n',
 'CUB007\t3\t0.526561592272\n',
 'CUB007\t4\t0.614952351345\n',
 'CUB007\t5\t0.619949914553\n',
 'CUB007\t6\t0.527194597272\n',
 'CUB007\t7\t0.546686640081\n',
 'CUB007\t8\t0.505733564855\n']

DATA_MATRIX = array([[ 0.53958482,  0.56818866,  0.56127714,  0.50657545,  0.        ,
         0.49336384,  0.50712689,  0.57622093,  0.49449403],
       [ 0.52165969,  0.56879946,  0.59490101,  0.59075898,  0.53158767,
         0.66923931,  0.63595568,  0.64049799,  0.63122263],
       [ 0.        ,  0.        ,  0.5114473 ,  0.48941173,  0.50750628,
         0.47626833,  0.51249147,  0.49501185,  0.46907879],
       [ 0.62648938,  0.57971443,  0.        ,  0.52656159,  0.61495235,
         0.61994991,  0.5271946 ,  0.54668664,  0.50573356]])


if __name__ == "__main__":
    main()
