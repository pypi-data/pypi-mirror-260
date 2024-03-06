#! /bin/bash -f

source /home/user/.setenv_pyenv38
/home/user/.pyenv/shims/python /common/python/suncasa-src/suncasa/eovsa/eovsa_pltQlookImage.py "$@"
