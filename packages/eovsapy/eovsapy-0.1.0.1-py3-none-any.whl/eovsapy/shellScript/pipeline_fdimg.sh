#! /bin/bash
/bin/bash /common/python/eovsapy/shellScript/pipeline.sh -c 1 > /tmp/pipeline.log 2>&1
/bin/bash /common/python/eovsapy/shellScript/pipeline_plt.sh > /tmp/pipeline_plt.log 2>&1
/bin/bash /common/python/eovsapy/shellScript/pipeline_compress.sh -n 1 -O 1 > /tmp/pipeline_compress.log 2>&1

