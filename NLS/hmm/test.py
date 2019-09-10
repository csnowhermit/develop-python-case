#! /usr/bin python
# encoding:utf-8

import numpy as np
from numpy import *
from NLS.hmm import gParam
from NLS.hmm.my_hmm import gmm_hmm

my_gmm_hmm = gmm_hmm()
my_gmm_hmm.loadWav(gParam.TRAIN_DATA_PATH)
# print len(my_gmm_hmm.samples[0])
my_gmm_hmm.hmm_start_train()
my_gmm_hmm.recog(gParam.TEST_DATA_PATH)
# my_gmm_hmm.melbank(24,256,8000,0,0.5,'m')
# my_gmm_hmm.mfcc(range(17280))
# my_gmm_hmm.enframe(range(0,17280),256,80)