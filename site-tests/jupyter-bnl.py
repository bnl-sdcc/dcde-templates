#!/bin/env python3

"""Clean-slate attempt 8/29/19 with John's configfactory output:"""

import parsl
import os
from parsl.config import Config

from parsl.channels import OAuthSSHChannel
from parsl.providers import CondorProvider
from parsl.launchers import SrunLauncher
from parsl.executors import HighThroughputExecutor
from parsl.addresses import address_by_hostname
from parsl.app.app import bash_app
from parsl.app.app import python_app

@python_app
def sdcc_wninfo():
    #import subprocess
    import os
    return os.uname()

#parsl.set_stream_logger()
#parsl.set_file_logger(AUTO_LOGNAME)
parsl.clear()

config = Config(
    app_cache=True,
    checkpoint_files=None,
    checkpoint_mode=None,
    checkpoint_period=None,
    data_management_max_threads=10,
    executors=[HighThroughputExecutor(
        address='',
        cores_per_worker=1.0,
        heartbeat_period=30,
        heartbeat_threshold=120,
        interchange_port_range=(55000, 56000),
        label='spce01.sdcc.bnl.gov-htcondor',
        launch_cmd='process_worker_pool.py {debug} {max_workers} -p {prefetch_capacity} -c {cores_per_worker}-m {mem_per_worker} --poll {poll_period} --task_url={task_url} --result_url={result_url} --logdir={logdir} --block_id={{block_id}} --hb_period={heartbeat_period} --hb_threshold={heartbeat_threshold} ',
        managed=True,
        max_workers=1,
        mem_per_worker=None,
        poll_period=10,
        prefetch_capacity=0,
        provider=CondorProvider(
            channel=OAuthSSHChannel(
                'spce01.sdcc.bnl.gov',
                envs={},
                port=2222,
                script_dir='/sdcc/u/dcde1000006/parsl_scripts',
                username='dcde1000006'
            ),
            environment={},
            init_blocks=1,
            # launcher=SingleNodeLauncher(),
            max_blocks=1,
            min_blocks=0,
            nodes_per_block=1,
            parallelism=1,
            project='',
            requirements='',
            scheduler_options='accounting_group = group_sdcc.main',
            transfer_input_files=[],
            walltime='00:10:00',
            worker_init='source /sdcc/u/dcde1000001/dcdesetup.sh'
        ),
        storage_access=[],
        suppress_failure=False,
        worker_debug=True,
        worker_logdir_root='/sdcc/u/dcde1000006/parsl_scripts/logs',
        worker_port_range=(50000, 51000),
        #worker_port_range=(5000, 5100),   # per John H's message 8/29/19
        worker_ports=None,
        working_dir='/sdcc/u/dcde1000006/parsl_scripts'
    )],
    lazy_errors=True,
    monitoring=None,
    retries=0,
    run_dir='runinfo',
    strategy='simple',
    usage_tracking=False
)


parsl.load(config)

#condorinfo = sdcc_wninfo(executors=['sdcc_condor'])
condorinfo = sdcc_wninfo()

print(condorinfo.result())
