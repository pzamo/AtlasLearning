#!/usr/bin/env python2.7
import sys
sys.path.append('/pbs/home/p/pzamolod/private/DB_management/')

from process_clean_files import *
input_path = root_path('/sps/atlas/p/portales/Jets/fullTrees/Zmm_truth/user.lportale.ZmmTruthV6cor_PowHegPythia8evgen_e3601_s3126_r9425_r9315.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu_hist', input_suffix = '.root', output_dir = '/sps/atlas/z/zamolod/DB/CUTTED/')
 # fullTrees/Zmm_truth/user.lportale.ZmmTruthV6cor_PowHegPythia8evgen_e3601_s3126_r9425_r9315.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu_hist'
# input_path = root_path('/sps/atlas/p/portales/Jets/fullTrees/Zmm_mc16d/user.lportale.Zmm_mc16d_MUact_DataSFcor_jetcalib_1.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu_hist', input_suffix = '.root', output_dir = '/sps/atlas/z/zamolod/DB/CUTTED/VAL/')

input_path.process_with_script('/pbs/home/p/pzamolod/private/DB_management/PreprocRoot.py', on_cc = True, name = 'CUTTING_proper_TT', ressources = 'vmem=10.0G,h_cpu=72:00:00,h_rss=10.0G', queue = 'huge', log_dir = '/pbs/home/p/pzamolod/logs')
