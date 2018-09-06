#!/usr/bin/env python2.7
import sys
sys.path.append('/pbs/home/p/pzamolod/private/DB_management')

from process_clean_files import *

batch = sys.argv[1]

output_directory = sys.argv[2]
batch_number = sys.argv[3]

batch = batch.split(',')
batch = [root_path(c, output_directory, input_suffix = '.root') for c in batch]
for i, btch in enumerate(batch):
	btch.preprocess_tree('jvttree', output_treeName = None, output_fileName = 'PreprocTree_{}_{}.root'.format(batch_number, i), max_clusters = 70, masking_length = 10)