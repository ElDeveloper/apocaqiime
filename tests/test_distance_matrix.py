#!/usr/bin/env python
# File created on 08 Jul 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, ApocaQIIME"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.7.0"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Use at your own risk"

from numpy import array
from cogent.util.unit_test import TestCase, main
from apocaqiime.distance_matrix import ratios_for_category

class TopLevelTests(TestCase):
    
    def setUp(self):
        self.crawford_mapping_file_headers = ['SampleID',
             'BarcodeSequence',
             'LinkerPrimerSequence',
             'Treatment',
             'DOB',
             'Description']
        self.crawford_mapping_file_data = [['PC.354',
              'AGCACGAGCCTA',
              'YATGCTGCCTCCCGTAGGAGT',
              'Control',
              '20061218',
              'Control_mouse_I.D._354'],
             ['PC.355',
              'AACTCGTCGATG',
              'YATGCTGCCTCCCGTAGGAGT',
              'Control',
              '20061218',
              'Control_mouse_I.D._355'],
             ['PC.356',
              'ACAGACCACTCA',
              'YATGCTGCCTCCCGTAGGAGT',
              'Control',
              '20061126',
              'Control_mouse_I.D._356'],
             ['PC.481',
              'ACCAGCGACTAG',
              'YATGCTGCCTCCCGTAGGAGT',
              'Control',
              '20070314',
              'Control_mouse_I.D._481'],
             ['PC.593',
              'AGCAGCACTTGT',
              'YATGCTGCCTCCCGTAGGAGT',
              'Control',
              '20071210',
              'Control_mouse_I.D._593'],
             ['PC.607',
              'AACTGTGCGTAC',
              'YATGCTGCCTCCCGTAGGAGT',
              'Fast',
              '20071112',
              'Fasting_mouse_I.D._607'],
             ['PC.634',
              'ACAGAGTCGGCT',
              'YATGCTGCCTCCCGTAGGAGT',
              'Fast',
              '20080116',
              'Fasting_mouse_I.D._634'],
             ['PC.635',
              'ACCGCAGAGTCA',
              'YATGCTGCCTCCCGTAGGAGT',
              'Fast',
              '20080116',
              'Fasting_mouse_I.D._635'],
             ['PC.636',
              'ACGGTGAGTGTC',
              'YATGCTGCCTCCCGTAGGAGT',
              'Fast',
              '20080116',
              'Fasting_mouse_I.D._636']]
        self.crawford_distance_matrix_headers = ['PC.636','PC.635','PC.356','PC.481','PC.354','PC.593','PC.355','PC.607','PC.634']

        self.crawford_distnace_matrix_data = array([
            # ['PC.636',   'PC.635'  ,   'PC.356' ,    'PC.481',    'PC.354',   'PC.593',    'PC.355',    'PC.607',    'PC.634']
            [ 0.        ,  0.61014333,  0.72232181,  0.62815324,  0.72251338, 0.74339063,  0.65734365,  0.69919064,  0.54115761],
            [ 0.61014333,  0.        ,  0.69657433,  0.65949405,  0.68786247, 0.74215598,  0.68926853,  0.64516597,  0.5819012 ],
            [ 0.72232181,  0.69657433,  0.        ,  0.6554139 ,  0.56636719, 0.69527523,  0.57360863,  0.72879089,  0.76386459],
            [ 0.62815324,  0.65949405,  0.6554139 ,  0.        ,  0.55626566, 0.66123424,  0.61017176,  0.66686216,  0.66300011],
            [ 0.72251338,  0.68786247,  0.56636719,  0.55626566,  0.        , 0.56819136,  0.56082803,  0.70222505,  0.75297701],
            [ 0.74339063,  0.74215598,  0.69527523,  0.66123424,  0.56819136, 0.        ,  0.6415118 ,  0.71039267,  0.75480369],
            [ 0.65734365,  0.68926853,  0.57360863,  0.61017176,  0.56082803, 0.6415118 ,  0.        ,  0.73250241,  0.70353983],
            [ 0.69919064,  0.64516597,  0.72879089,  0.66686216,  0.70222505, 0.71039267,  0.73250241,  0.        ,  0.72119667],
            [ 0.54115761,  0.5819012 ,  0.76386459,  0.66300011,  0.75297701, 0.75480369,  0.70353983,  0.72119667,  0.        ]])


        self.mapping_file_headers = ['SampleID', 'Category', 'Something']
        self.mapping_file_data = [['a', 'cat_1', 'foo'], ['b', 'cat_2',
            'bar'], ['c', 'cat_1', 'baz'], ['d', 'cat_2', 'spam'], ['e',
            'cat_1', 'bazcam']]
                                        #1    2    2    1    1
        self.distance_matrix_headers = ['a', 'b', 'd', 'c', 'e']
        self.distance_matrix_data = array([ [0, 0.1, 0.3, 0.15, 0.20],
                                            [0.1, 0, 0.4, 0.112, 0.3],
                                            [0.3, 0.4, 0, 0.455, 0.9],
                                            [0.15, 0.112, 0.455, 0, 0.21],
                                            [0.20, 0.3, 0.9, 0.21, 0]])

        # 1:0+0+1
        # 2:0+0
    def test_ratios_for_category(self):
        """ """
        output_dict = ratios_for_category(self.crawford_distance_matrix_headers,
            self.crawford_distnace_matrix_data, self.crawford_mapping_file_headers,
            self.crawford_mapping_file_data, 'Treatment')
        self.assertEquals(output_dict, {'Control': (5, 5), 'Fast': (4,4)})

        output_dict = ratios_for_category(self.distance_matrix_headers,
            self.distance_matrix_data, self.mapping_file_headers,
            self.mapping_file_data, 'Category')
        self.assertEquals(output_dict, {'cat_1': (1,3), 'cat_2': (0,2)})


if __name__ == "__main__":
    main()