#!/bin/env python
#
#

import sys
sys.path.append('/direct/sdcc+u/dcde1000006/sc19-demo/bnl')

import parsl
import os
#from parsl.config import Config
from bnl_config_dirty import bnl_sdcc_config

# Thought I'd get all these from the config above, but maybe not:
from parsl.channels import OAuthSSHChannel
from parsl.providers import CondorProvider
from parsl.launchers import SrunLauncher
from parsl.executors import HighThroughputExecutor
from parsl.addresses import address_by_hostname
from parsl.app.app import bash_app
from parsl.app.app import python_app

#print(parsl.__version__) # We expect parsl master branch 0.8.0 (10/8/19) for this notebook

#config = bnl_config_dirty.bnl_sdcc_config
config = bnl_sdcc_config
parsl.load(config)

# The bash_app will run on a worker node

@bash_app
def bnl_node_probe(job_dir=None, stdout=None, stderr=None, mock=True):
    cmd_line = '''pwd
echo $HOME
/bin/ls $HOME
/bin/df -h
    '''
    return cmd_line


if __name__ == "__main__":

    """FIXME: I think we need to set a common working dir for local and remote proceses! 
    is that in config? """

    #parsl.set_stream_logger()
    w = bnl_node_probe(stdout='nodeprobe.out', stderr='nodeprobe.err')
    w.result()
    if w.done():
        with open(w.stdout, 'r') as f:
            print(f.read())

    sys.exit() 
