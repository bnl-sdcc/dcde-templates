parsl.clear()

parsl.load(anl_config)
anl_dfk = parsl.dfk()
#print(anl_dfk.executors)

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

singularity exec  -B /blues/gpfs/home:/blues/gpfs/home ${{RELION_SIMG}} relion_autopick --i ${{INSTAR}} --ref ${{REFSTAR}} --odir ${{PICKDIR}} --pickname autopick --invert  --ctf  --ang 5 --shrink 0 --lowpass 20 --particle_diameter 200 --threshold 0.4 --min_distance 110 --max_stddev_noise 1.1
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

relion_stdout=os.path.join(anl_config.executors[0].working_dir, 'relion-anl-autopick.out')
relion_stderr=os.path.join( anl_config.executors[0].working_dir, 'relion-anl-autopick.err')

#local_logdir='/blues/gpfs/home/dcowley/sc19-data/parsl-outputs'
# This is local to BNL!
local_logdir= '/hpcgpfs01/scratch/dcde1000006/sc19-data/parsl-outputs'

local_logfile=os.path.join(local_logdir, 'relion-anl-autopick.out')

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
try:
    os.remove(local_logfile)
except OSError:
    pass
except FileNotFoundError:
    pass

print ('job setup: stdout = {}\nstderr = {}'.format(relion_stdout,relion_stderr))
# parsl.set_stream_logger()
# Call Relion and wait for results

x = relion_autopick(stdout=relion_stdout, stderr=relion_stderr, mock = False)
print('relion_autopick() invoked, now waiting...')
x.result()
print('relion_autopick() returned, output should print below:')

#if x.done():
if True:
    anl_dfk.executors['anl-slurm'].provider.channel.pull_file(relion_stdout, local_logdir)
    with open(local_logfile, 'r') as f:
        print(f.read())
