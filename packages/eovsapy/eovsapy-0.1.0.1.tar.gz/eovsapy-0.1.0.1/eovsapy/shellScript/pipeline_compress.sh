#! /bin/bash -f

#set up python path variable, and path to Anaconda Python
source /home/user/.setenv_pyenv38
/home/user/.pyenv/shims/python /common/python/suncasa-src/suncasa/eovsa/eovsa_fitsutils.py "$@"

