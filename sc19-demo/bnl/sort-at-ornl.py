
parsl.clear()

parsl.load(ornl_config)
ornl_dfk = parsl.dfk()
#print(ornl_dfk.executors)


@bash_app
def sort_at_ornl(job_dir=None, stdout=None, stderr=None, mock=True):
    """
    Parameters
    ----------
    mock : (Bool)
       when mock=True
    """
    cmd_line = '''#!/bin/bash -l
export DATAROOT=/nfs/scratch/sc19-demo
export RELION_SIMG=/nfs/sw/relion/relion_singv26.simg

export INSTAR=${{DATAROOT}}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${{DATAROOT}}/Select/job007/class_averages.star
export PICKDIR=${{DATAROOT}}/AutoPick/job010/
export PARTSTAR=${{DATAROOT}}/Extract/job011/particles.star
export SORTSTAR=${{DATAROOT}}/Sort/job012/particles_sort.star

echo -n "working directory: "
pwd
set -v

singularity exec -B ${{DATAROOT}}:${{DATAROOT}} $RELION_SIMG relion_particle_sort --i ${{PARTSTAR}} --ref ${{REFSTAR}} --o ${{SORTSTAR}} --ctf
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

relion_stdout=os.path.join(anl_config.executors[0].working_dir, 'relion-ornl-sort.out')

relion_stderr=os.path.join( anl_config.executors[0].working_dir, 'relion-ornl-sort.err')

# This is local to BNL
local_logdir= '/hpcgpfs01/scratch/dcde1000006/sc19-data/parsl-outputs'

local_logfile=os.path.join(local_logdir, 'relion-anl-sort.out')

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

print ('job setup: \nstdout = {}\nstderr = {}'.format(relion_stdout,relion_stderr))
# parsl.set_stream_logger()
# Call Relion and wait for results

x = relion_sort_at_ornl(stdout=relion_stdout, stderr=relion_stderr, mock = True )
print('relion_sort_at_ornl() invoked, now waiting...')
x.result()

if x.done():
    with open(x.stdout, 'r') as f:
        print(f.read())
