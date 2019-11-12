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
                script_dir='/home/dcowley/ornl-parsl-scripts',
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
            scheduler_options='#SBATCH -A dcde\n#SBATCH -t 0:20:00\n#SBATCH -N 1\n#SBATCH --ntasks-per-node=36\n#SBATCH -J relion-autopick\n#SBATCH -p bdwall\n#SBATCH -D /blues/gpfs/home/dcowley/relion-bootstrap\n#SBATCH -o relion-autopick.%j.out\n#SBATCH -e relion-autopick.%j.err',
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



parsl.load(config)
dfk = parsl.dfk()
print(dfk)

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

export DATAROOT=/blues/gpfs/home/dcowley/relion-bootstrap
export RELION_SIMG=/lcrc/project/DCDE/relion/relion_singv26.simg

export INSTAR=${{DATAROOT}}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${{DATAROOT}}/Select/job007/class_averages.star
export PICKDIR=${{DATAROOT}}/AutoPick/job010/

echo -n "working directory: "
pwd
module load singularity/2.6.0
set -v

singularity exec  -B /blues/gpfs/home:/blues/gpfs/home $RELION_SIMG relion_autopick --i $INSTAR --ref $REFSTAR --odir $PICKDIR --pickname autopick --invert  --ctf  --ang 5 --shrink 0 --lowpass 20 --particle_diameter 200 --threshold 0.4 --min_distance 110 --max_stddev_noise 1.1 # --gpu "0"
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

    anlhome='/home/dcowley'
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
    """
    Take a look back at https://github.com/Parsl/demo_multifacility.

    Where are stderr, stdout going..!?  parsl.log (on the client machine) says
    it's available the bare filename I specify, apparently on the client at jupyterhub..

    NOPE!  They're on argonne in  /blues/gpfs/dcowley/relion-bootstrap, which is
    #SBATCH -D for the job that starts the..  interchange?

    The job seems to break (slurmstepd: error: *** JOB 1317025 ON bdw-0524
    CANCELLED AT 2019-11-11T22:43:53 ***), possibly because the client pukes on
    file not found error on 'relion-anl-autopick.out' (which again is on the
    remote machine).  Do I need to stage these files?

    The developers guide seems to say that the DFK's execute_wait() functions
    handle stderr,  stdin, stdout and call the channels.  "For channels that
    execute remotely, a push_file function allows you to copy over files."

    **oauth_ssh channel does not have push_file!!**


    """
    x = relion_autopick(stdout=relion_stdout, stderr=relion_stderr, mock = False)
    print('relion_autopick() invoked, now wating...')
    x.result()

    if x.done():
        # obsolete:
        #dfk.executor.execution_provider.channel.pull_file(relion_stdout, '.')
        dfk.executors['anl-slurm'].provider.channel.pull_file(relion_stdout, '.')
        #with open(x.stdout, 'r') as f:
        with open(relion_stdout, 'r') as f:
            print(f.read())
