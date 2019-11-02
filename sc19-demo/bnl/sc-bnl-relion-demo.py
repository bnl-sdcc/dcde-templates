#!/bin/env python
#
#


import sys
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

print(parsl.__version__) # We expect parsl master branch 0.8.0 (10/8/19) for this notebook

config = Config(
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
        #interchange_port_range=(55000, 56000),
        label='spce01.sdcc.bnl.gov-htcondor',
        launch_cmd='process_worker_pool.py {debug} {max_workers} -p {prefetch_capacity} -c {cores_per_worker} -m {mem_per_worker} --poll {poll_period} --task_url={task_url} --result_url={result_url} --logdir={logdir} --block_id={{block_id}} --hb_period={heartbeat_period} --hb_threshold={heartbeat_threshold} ',
        mem_per_worker=4,
        managed=True,
        max_workers=1,
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
            #worker_init='source /sdcc/u/dcde1000001/dcdesetup.sh'
            worker_init='source /hpcgpfs01/work/dcde/setup.sh; source activate dcdemaster20191008'
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



# THIS IS ONLY A PLACEHOLDER CONFIG TO GET THIS QUICKLY TESTED

parsl.load(config)

# The bash_app will run on a worker node
@bash_app
def relion_refine_mpi(job_dir=None, stdout=None, stderr=None, mock=True):
    """
    Parameters
    ----------
    mock : (Bool)
       when mock=True
    """
    cmd_line = '''
set -v
# $HOME is apparently NOT set by condor!

#env

echo
uname -a
df -h
echo

export SCRATCHDIR="/hpcgpfs01/scratch/dcde1000006"
export JOBDIR="${SCRATCHDIR}/parsl_jobs/${JOBNAME}"
export DATAROOT="${SCRATCHDIR}/relion-tut/relion21_tutorial/PrecalculatedResults"

mkdir $JOBDIR
cd $JOBDIR

mkdir ${JOBDIR}/Class3D || exit
ln -s ${DATAROOT}/Extract Extract || exit
ln -s ${DATAROOT}/Select Select || exit

echo  "HOME is: $HOME"
echo  "SCRATCHDIR is: $SCRATCHDIR"
echo  "JOBDIR is: $JOBDIR"
echo  "DATAROOT is: $DATAROOT"
echo

echo "DATAROOT contents:"
ls -al $DATAROOT
echo

echo "JOBDIR contents:"
ls -al $JOBDIR
echo

echo "Class3d contents:"
ls -al ${JOBDIR}/Class3D
echo

echo -n "PWD is: " 
pwd
echo

singularity exec -B /hpcgpfs01:/hpcgpfs01 ${SCRATCHDIR}/relion_singv26.simg mpirun -n 16 /usr/local/bin/relion_refine_mpi \
    --o ${JOBDIR}/Class3D  \
    --i ${DATAROOT}/Select/after_sorting/particles.star  \
    --ref ${DATAROOT}/InitialModel/symC1/inimodel_symD2.mrc  \
    --ini_high 50  \
    --dont_combine_weights_via_disc  \
    --preread_images   \
    --pool 3  \
    --ctf  \
    --ctf_corrected_ref  \
    --iter 4  \
    --tau2_fudge 4  \
    --particle_diameter 200  \
    --K 4  \
    --flatten_solvent  \
    --zero_mask  \
    --oversampling 1  \
    --healpix_order 2  \
    --offset_range 5  \
    --offset_step 2  \
    --sym C1  \
    --norm  \
    --scale   \
    --j 1

set +v 
date

echo "****************************************"

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

    relion_stdout=os.path.join(os.environ['HOME'], 'relion.out')
    relion_stderr=os.path.join(os.environ['HOME'], 'relion.err')

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
    parsl.set_stream_logger()
    # Call Relion and wait for results
    x = relion_refine_mpi(stdout=relion_stdout, stderr=relion_stderr, mock = False )
    x.result()

    if x.done():
        with open(x.stdout, 'r') as f:
            print(f.read())

    sys.exit()
