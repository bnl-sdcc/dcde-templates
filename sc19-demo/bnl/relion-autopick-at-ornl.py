#!/bin/env python

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



#parsl.set_file_logger(filename='parsl-anl-slurm-log')
#parsl.set_stream_logger()


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
        interchange_port_range=(50000, 51000),
        label='ornl-slurm',
        launch_cmd='process_worker_pool.py {debug} {max_workers} -p {prefetch_capacity} -c {cores_per_worker} -m {mem_per_worker} --poll {poll_period} --task_url={task_url} --result_url={result_url} --logdir={logdir} --block_id={{block_id}} --hb_period={heartbeat_period} --hb_threshold={heartbeat_threshold} ',
        managed=True,
        max_workers=1,
        #mem_per_worker=None,
        poll_period=10,
        prefetch_capacity=0,
        interchange_address='128.219.185.39', #this is the address worker talk to inetrchange(head node)
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
            max_blocks=1,
            min_blocks=1,
            move_files=True,
            nodes_per_block=1,
            parallelism=0.0,
            #scheduler_options='#SBATCH -A dcde\n#SBATCH -t 0:20:00\n#SBATCH -N 1\n#SBATCH --ntasks-per-node=36\n#SBATCH -J relion-autopick\n#SBATCH -p bdwall\n#SBATCH -D /blues/gpfs/home/dcowley/relion-bootstrap\n#SBATCH -o relion-autopick.%j.out\n#SBATCH -e relion-autopick.%j.err',
            scheduler_options='#SBATCH -D /nfs/scratch/relion-bootstrap'
            walltime='00:10:00',
            worker_init='source /nfs/scratch/dcde1000012/RX.sh'
        ),
        storage_access=[],
        suppress_failure=False,
        worker_debug=True,
        worker_logdir_root='/home/dcde1000006/parsl_scripts/logs',
        worker_port_range=(50000, 51000),
        #worker_ports=None,
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

@bash_app
def relion_autopick(job_dir=None, stdout=None, stderr=None, mock=True):
    """
    Parameters
    ----------
    mock : (Bool)
       when mock=True
    """
    cmd_line = '''#!/bin/bash -l

export I_MPI_FABRICS=shm:tmi

export DATAROOT=/nfs/scratch/relion-bootstrap
export RELION_SIMG=/nfs/sw/relion/relion_singv26.simg

export INSTAR=${{DATAROOT}}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${{DATAROOT}}/Select/job007/class_averages.star
export PICKDIR=${{DATAROOT}}/AutoPick/job010/

echo -n "working directory: "
pwd
# module load singularity/2.6.0
set -v

# output directory /nfs/scratch/relion-bootstrap:/

singularity exec -B /nfs/scratch/relion-bootstrap:/nfs/scratch/relion-bootstrap $RELION_SIMG relion_autopick --i $INSTAR --ref $REFSTAR --odir $PICKDIR --pickname autopick --invert  --ctf  --ang 5 --shrink 0 --lowpass 20 --particle_diameter 200 --threshold 0.4 --min_distance 110 --max_stddev_noise 1.1 # --gpu "0"
    '''
    if mock:
        return '''tmp_file=$(mktemp);
cat<<EOF > $tmp_file
{}
EOF
cat $tmp_file
        '''.format(cmd_line)
    else:
        return cmd_line



if __name__ == "__main__":

    #anlhome='/home/dcowley'
    #relion_stdout=os.path.join(os.environ['HOME'], 'relion.out')
    #relion_stderr=os.path.join(os.environ['HOME'], 'relion.err')
    #relion_stdout=os.path.join(anlhome, 'relion.out')
    #relion_stderr=os.path.join(anlhome, 'relion.err')
    relion_stdout='relion-anl-autopick.out'
    relion_stderr='relion-anl-autopick.err'

    try:
        os.remove(relion_stdout)
    except OSError:
        pass
    except FileNotFoundError:
        pass
    try:
        os.remove(relion_stderr)
    except OSError:
        pass
    except FileNotFoundError:
        pass


    print ('job setup: stdout = {}\nstderr = {}'.format(relion_stdout,relion_stderr))
    # parsl.set_stream_logger()
    # Call Relion and wait for results
    
    print('relion_autopick() invoked, now wating...')
    x.result()

    if x.done():
        with open(x.stdout, 'r') as f:
            print(f.read())
