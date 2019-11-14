parsl.clear()

#parsl.set_stream_logger()
parsl.load(bnl_config)
bnl_dfk = parsl.dfk()

@bash_app
def relion_import(job_dir=None, stdout=None, stderr=None, mock=True):
    """
    Parameters
    ----------
    mock : (Bool)
       when mock=True
    """
    cmd_line = '''#!/bin/bash -l

export DATAROOT=/hpcgpfs01/scratch/dcde1000006/sc19-data
export RELION_SIMG=/lcrc/project/DCDE/relion/relion_singv26.simg

export INSTAR=${{DATAROOT}}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${{DATAROOT}}/Select/job007/class_averages.star
export PICKDIR=${{DATAROOT}}/AutoPick/job010/

echo -n "working directory: "
pwd
set -v

singularity exec  -B /hpcgpfs01:/hpcgpfs01 ${{RELION_SIMG}} relion_star_loopheader rlnMicrographMovieName > $MOVIESTAR
singularity exec  -B /hpcgpfs01:/hpcgpfs01 ${{RELION_SIMG}} ls Micrographs/*.mrcs >> $MOVIESTAR
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


relion_stdout=os.path.join(bnl_config.executors[0].working_dir, 'relion-bnl-import.out')
relion_stderr=os.path.join( bnl_config.executors[0].working_dir, 'relion-bnl-import.err')

demo_outdir='/hpcgpfs01/scratch/dcde1000006/sc19-data/parsl-outputs'

"""
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
"""


print ('job setup: stdout = {}\nstderr = {}'.format(relion_stdout,relion_stderr))
# parsl.set_stream_logger()

x = relion_import(job_dir=bnl_config.executors[0].working_dir, stdout=relion_stdout, stderr=relion_stderr, mock = True)
print('relion_import() invoked, now waiting...')
x.result()

if x.done():
    bnl_dfk.executors['bnl-condor'].provider.channel.pull_file(relion_stdout, demo_outdir)
    #with open(x.stdout, 'r') as f:
    #with open(relion_stdout, 'r') as f:
    # FIXME: fix path handling here:
    #with open('relion-bnl-import.out', 'r') as f:
    with open(relion_stdout, 'r') as f:
        print(f.read())
