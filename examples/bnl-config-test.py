#!/usr/bin/env python3

import argparse
import logging
import parsl

from parsl.app.app import python_app, bash_app
from parsl.executors.ipp_controller import Controller
from parsl.channels.local.local import LocalChannel
from parsl.providers import CondorProvider
from parsl.config import Config
from parsl.executors import HighThroughputExecutor
from dcdeparsl.configfactory import ConfigFactory

@python_app
def worker_info():
    #import subprocess
    import os
    return os.uname()



if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s (UTC) [%(levelname)s] %(name)s %(filename)s:%(lineno)d %(funcName)s(): %(message)s')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conffile', 
                        action="store", 
                        dest='conffile', 
                        default="/etc/dcde/dcdeparsl.conf",
                        help='configuration file.')

    parser.add_argument('-u', '--username', 
                        action="store", 
                        dest='username', 
                        default="dcde1000001",
                        help='remote username')

    parser.add_argument('-e', '--endpoint', 
                        action="store", 
                        dest='endpoint', 
                        default="spce01.sdcc.bnl.gov",
                        help='remote submit host')

    parser.add_argument('-v', '--verbose', 
                        action="store_true", 
                        dest='verbose', 
                        help='verbose (info) logging')

    
    parser.add_argument('-d', '--debug', 
                        action="store_true", 
                        dest='debug', 
                        help='debug logging')
    
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s (UTC) [%(levelname)s] %(name)s %(filename)s:%(lineno)d %(funcName)s(): %(message)s')
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARN)
    
       
    #parsl.set_stream_logger(level=0)
    parsl.clear()
    
    logging.info("getting configfactory with conffile: %s" %  args.conffile)
    cf = ConfigFactory(conffile=args.conffile)
    logging.info("getting config for spce01.sdcc.bnl.gov, dcde1000001")
    bnl_sdcc_condor = cf.getconfig( args.endpoint, args.username)
    
    logging.info("loading config: %s" % bnl_sdcc_condor)
    
    parsl.load(bnl_sdcc_condor)

    logging.info("submitting...")
  
  
    # Must. wait. for. job. to. finish.
    result = worker_info().result()
    print(result)
    print("result type: %s" % type(result))
    
    logging.info("got result, printing...")

    

