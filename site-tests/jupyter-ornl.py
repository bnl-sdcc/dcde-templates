#!/bin/env python
"""
Fresh attempt 8/29/19 PM.  Take john's configfactory-generated config and see if
we can do anything with it:
"""

import parsl
import os
from parsl.config import Config

from parsl.channels import OAuthSSHChannel
from parsl.providers import SlurmProvider
from parsl.launchers import SrunLauncher
from parsl.executors import HighThroughputExecutor
from parsl.addresses import address_by_hostname
from parsl.app.app import bash_app
from parsl.app.app import python_app

@python_app()
def worker_info():
    #import subprocess
    import os
    return os.uname()



parsl.set_file_logger(filename='parsl-ornl-slurm-log')


config = Config(
    app_cache=True,
    checkpoint_files=None,
    checkpoint_mode=None,
    checkpoint_period=None,
    data_management_max_threads=10,
    executors=[HighThroughputExecutor(
        address='130.199.185.13',
        cores_per_worker=1.0,
        heartbeat_period=30,
        heartbeat_threshold=120,
        interchange_port_range=(55000, 56000),
        label='dcde-ext.ornl.gov-slurm',
        launch_cmd='process_worker_pool.py {debug} {max_workers} -p {prefetch_capacity} -c {cores_per_worker} -m {mem_per_worker} --poll {poll_period} --task_url={task_url} --result_url={result_url} --logdir={logdir} --block_id={{block_id}} --hb_period={heartbeat_period} --hb_threshold={heartbeat_threshold} ',
        managed=True,
        max_workers=1,
        mem_per_worker=None,
        poll_period=10,
        prefetch_capacity=0,
        provider=SlurmProvider(
            'debug',
            channel=OAuthSSHChannel(
                'dcde-ext.ornl.gov',
                envs={},
                port=2222,
                script_dir='/home/dcde1000006/ornl-parsl-scripts',
                username='dcde1000006'
            ),
            cmd_timeout=10,
            exclusive=True,
            init_blocks=1,
            # launcher=SingleNodeLauncher(),
            max_blocks=10,
            min_blocks=0,
            move_files=True,
            nodes_per_block=1,
            parallelism=1,
            scheduler_options='#SBATCH --exclusive\naccounting_group = group_sdcc.main',
            walltime='00:10:00',
            worker_init='source /home/dcde1000001/dcdesetup.sh'
        ),
        storage_access=[],
        suppress_failure=False,
        worker_debug=True,
        worker_logdir_root='/home/dcde1000006/parsl_scripts/logs',
        worker_port_range=(50000, 51000),
        worker_ports=None,
        working_dir='/home/dcde1000006/parsl_scripts'
    )],
    lazy_errors=True,
    monitoring=None,
    retries=0,
    run_dir='runinfo',
    strategy='simple',
    usage_tracking=False
)


parsl.load(config)

result = worker_info().result()
print(result)
print("result type: %s" % type(result))
