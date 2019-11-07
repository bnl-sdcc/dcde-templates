
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
    cmd_line = '''#!/bin/bash -l

echo "****************************************"
date
whoami
id
hostname
which singularity
date

echo -n "initial directory:"
pwd
echo -n "contents:"
ls


#export HOME=/direct/usatlas+grid/dcde1000006
export HOME=/usatlas/grid/dcde1000006
#env
echo "contents of $HOME:"
ls -l $HOME

DATAROOT=${HOME}/relion-tut/relion21_tutorial/PrecalculatedResults
echo "\$DATAROOT: $DATAROOT"
#ls $DATAROOT

mkdir -p PostProcess/$$/postprocess || exit
#ln -s ${DATAROOT}/MaskCreate MaskCreate
#ln -s ${DATAROOT}/Refine3D Refine3D

echo -n "working directory:"
pwd
echo -n "contents:"
ls


singularity exec ${HOME}/relion_singv26.simg /usr/local/bin/relion_postprocess --mask ${DATAROOT}/MaskCreate/first3dref_th002_ext2_edg3/mask.mrc --i ${DATAROOT}/Refine3D/after_first_class3d/run  --angpix 3.54 --mtf ${DATAROOT}/mtf_falcon2_300kV.star --auto_bfac  --autob_lowres 10

pwd
ls -l

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



################

#!/bin/bash

#SBATCH -A dcde
#SBATCH -t 0:20:00
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -J relion-autopick
#SBATCH -p bdwall
#SBATCH -D /blues/gpfs/home/dcowley/relion-bootstrap
#SBATCH -o relion-autopick.%j.out
#SBATCH -e relion-autopick.%j.err
#SBATCH --mail-user=david.cowley@pnnl.gov



export I_MPI_FABRICS=shm:tmi


export DATAROOT=/blues/gpfs/home/dcowley/relion-bootstrap

export INSTAR=${DATAROOT}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${DATAROOT}/Select/job007/class_averages.star
export PICKDIR=${DATAROOT}/AutoPick/job010/


echo -n "working directory: "
pwd

module load singularity/2.6.0

set -v

touch run.start

singularity exec  -B /blues/gpfs/home:/blues/gpfs/home ${HOME}/relion_singv26.simg relion_autopick --i $INSTAR --ref $REFSTAR --odir $PICKDIR --pickname autopick --invert  --ctf  --ang 5 --shrink 0 --lowpass 20 --particle_diameter 200 --threshold 0.4 --min_distance 110 --max_stddev_noise 1.1 # --gpu "0"
touch run.stop
