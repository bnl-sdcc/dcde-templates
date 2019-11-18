

import parsl
import os
from parsl.config import Config


from parsl.channels import OAuthSSHChannel
from parsl.providers import CondorProvider
from parsl.providers import SlurmProvider
from parsl.launchers import SrunLauncher
from parsl.executors import HighThroughputExecutor
from parsl.addresses import address_by_hostname
from parsl.app.app import bash_app
from parsl.app.app import python_app



anl_config = Config(
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
        interchange_port_range=(50000, 51000),
        label='anl-slurm',
        launch_cmd='process_worker_pool.py {debug} {max_workers} -p {prefetch_capacity} -c {cores_per_worker} -m {mem_per_worker} --poll {poll_period} --task_url={task_url} --result_url={result_url} --logdir={logdir} --block_id={{block_id}} --hb_period={heartbeat_period} --hb_threshold={heartbeat_threshold} ',
        managed=True,
        max_workers=1,
        #mem_per_worker=None,
        poll_period=10,
        prefetch_capacity=0,
        interchange_address='10.70.128.9', #this is the address worker talk to inetrchange(head node)
        provider=SlurmProvider(
            'debug',
            channel=OAuthSSHChannel(
                'gssh.lcrc.anl.gov',
                envs={},
                port=2222,
                script_dir='/home/dcowley/anl-parsl-scripts',
                username='dcowley'
            ),
            cmd_timeout=10,
            exclusive=True,
            init_blocks=1,
            # launcher=SingleNodeLauncher(),
            max_blocks=1,
            min_blocks=1,
            move_files=True,
            nodes_per_block=1,
            parallelism=0.0,
            scheduler_options='#SBATCH -A dcde\n#SBATCH -t 0:20:00\n#SBATCH -N 1\n#SBATCH --ntasks-per-node=36\n#SBATCH -J relion-autopick\n#SBATCH -p bdwall\n#SBATCH -D /blues/gpfs/home/dcowley/sc19-demo\n#SBATCH -o relion-autopick.%j.out\n#SBATCH -e relion-autopick.%j.err',
            walltime='00:10:00',
            #worker_init='source /home/dcde1000001/dcdesetup.sh'
            worker_init='source /lcrc/project/DCDE/setup.sh;  source activate /lcrc/project/DCDE/envs/dcdeRX; export I_MPI_FABRICS=shm:tmi'
        ),
        storage_access=[],
        suppress_failure=False,
        worker_debug=True,
        worker_logdir_root='/home/dcowley/parsl_scripts/logs',
        worker_port_range=(50000, 51000),
        #worker_ports=None,
        working_dir='/home/dcowley/parsl_scripts'
    )],
    lazy_errors=True,
    monitoring=None,
    retries=0,
    run_dir='runinfo',
    strategy='simple',
    usage_tracking=False
)

print("ANL Parsl config loaded.")

bnl_config = Config(
    app_cache=True,
    checkpoint_files=None,
    checkpoint_mode=None,
    checkpoint_period=None,
    data_management_max_threads=10,
    executors=[HighThroughputExecutor(
        #address='127.0.0.1',
        address='130.199.185.13',
        cores_per_worker=1,
        heartbeat_period=30,
        heartbeat_threshold=120,
        interchange_port_range=(50000, 51000),
        label='bnl-condor',
        launch_cmd='process_worker_pool.py {debug} {max_workers} -p {prefetch_capacity} -c {cores_per_worker} -m {mem_per_worker} --poll {poll_period} --task_url={task_url} --result_url={result_url} --logdir={logdir} --block_id={{block_id}} --hb_period={heartbeat_period} --hb_threshold={heartbeat_threshold} ',
        mem_per_worker=4,
        managed=True,
        max_workers=1,
        poll_period=10,
        prefetch_capacity=0,
        interchange_address='130.199.185.9', #this is the address worker talk to inetrchange(head node)
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
            min_blocks=1,
            nodes_per_block=1,
            #parallelism=1,
            parallelism=0,
            project='',
            #Trying this Requirements directive per Dong's instructions:
            #requirements='regexp("^sp[oa]", machine)',
            scheduler_options='accounting_group = group_sdcc.main \nRequirements = (regexp("^sp[oa]", machine))',
            transfer_input_files=[],
            walltime='00:30:00',
            #worker_init='source /hpcgpfs01/work/dcde/setup.sh; source activate dcdemaster20191008'
            worker_init='source /hpcgpfs01/work/dcde/setup.sh; source activate dcdeRX'
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

print("BNL Parsl config loaded.")

ornl_config = Config(
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
        interchange_port_range=(50000, 51000),
        label='ornl-slurm',
        launch_cmd='process_worker_pool.py {debug} {max_workers} -p {prefetch_capacity} -c {cores_per_worker} -m {mem_per_worker} --poll {poll_period} --task_url={task_url} --result_url={result_url} --logdir={logdir} --block_id={{block_id}} --hb_period={heartbeat_period} --hb_threshold={heartbeat_threshold} ',
        managed=True,
        max_workers=1,
        #mem_per_worker=None,
        poll_period=10,
        prefetch_capacity=0,
        interchange_address='128.219.185.39', #this is the address worker talk to interchange (head node)
        provider=SlurmProvider(
            'debug',
            channel=OAuthSSHChannel(
                'dcde-ext.ornl.gov',
                envs={},
                port=2222,
                #script_dir='/home/dcde1000006/ornl-parsl-scripts',
                script_dir='/nfs/scratch/dcde1000006/ornl-parsl-scripts',
                username='dcde1000006'
            ),
            cmd_timeout=10,
            exclusive=True,
            init_blocks=1,
            # launcher=SingleNodeLauncher(),
            max_blocks=1,
            min_blocks=1,
            move_files=True,
            nodes_per_block=1,
            parallelism=0.0,
            scheduler_options='#SBATCH -D /nfs/scratch/sc19-data\n#SBATCH -o relion-autopick.%j.out\n#SBATCH -e relion-autopick.%j.err',
            walltime='00:10:00',
            worker_init='source /nfs/scratch/dcde1000012/RX.sh'
        ),
        storage_access=[],
        suppress_failure=False,
        worker_debug=True,
        worker_logdir_root='/nfs/scratch/dcde1000006/parsl_scripts/logs',
        worker_port_range=(50000, 51000),
        #worker_ports=None,
        working_dir='/nfs/scratch/dcde1000006/parsl_scripts'
    )],
    lazy_errors=True,
    monitoring=None,
    retries=0,
    run_dir='runinfo',
    strategy='simple',
    usage_tracking=False
)

print("ORNL Parsl config loaded.")

ANL_EP = '57b72e31-9f22-11e8-96e1-0a6d4e044368'
BNL_EP = '23f78cc8-41e0-11e9-a618-0a54e005f950'
EMSL_EP = 'e133a52e-6d04-11e5-ba46-22000b92c6ec'
ORNL_EP = '57230a10-7ba2-11e7-8c3b-22000b9923ef'
