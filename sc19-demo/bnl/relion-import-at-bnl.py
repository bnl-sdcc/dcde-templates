parsl.clear()

#parsl.set_stream_logger()
parsl.load(bnl_config)
# Note: clear(), load(), dfk() are in DataFlowKernelLoader (dflow.py)
bnl_dfk = parsl.dfk()

@bash_app
def relion_import(job_dir=None, stdout=None, stderr=None, mock=False):
    """
    Parameters
    ----------
    mock : (Bool)
       when mock=True
    """
    cmd_line = '''#!/bin/bash -l

export DATAROOT=/hpcgpfs01/scratch/dcde1000006/sc19-data
export RELION_SIMG=/sdcc/u/dcde1000006/relion_singv26.simg

export MOVIESTAR=Import/job001/movies.star
export INSTAR=CtfFind/job003/micrographs_ctf.star
export REFSTAR=Select/job007/class_averages.star
export PICKDIR=AutoPick/job010/

cd ${{DATAROOT}}
echo -n "working directory: "
pwd
set -v

singularity exec -W ${{DATAROOT}} -B /hpcgpfs01:/hpcgpfs01 ${{RELION_SIMG}} relion_star_loopheader rlnMicrographMovieName > ${{MOVIESTAR}}
singularity exec -W ${{DATAROOT}} -B /hpcgpfs01:/hpcgpfs01 ${{RELION_SIMG}} ls Micrographs/*.mrcs >> ${{MOVIESTAR}}

echo "Wrote file ${{MOVISTAR}}:"; echo
cat ${{MOVIESTAR}}

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

local_logdir='/hpcgpfs01/scratch/dcde1000006/sc19-data/parsl-outputs'
local_logfile=os.path.join(local_logdir, 'relion-bnl-import.out')

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

x = relion_import(job_dir=bnl_config.executors[0].working_dir, stdout=relion_stdout, stderr=relion_stderr, mock = False)
print('relion_import() invoked, now waiting...')
x.result()
print('relion_import() invoked has finished, output should print now:')

if True:
    bnl_dfk.executors['bnl-condor'].provider.channel.pull_file(relion_stdout, local_logdir)
    with open(local_logfile, 'r') as f:
        print(f.read())

# Try to shut down if we're done
if x.done():
    print('parsl done() call returned True.  Trying to shut down executor...')
    bnl_dfk.executors['bnl-condor'].shutdown()
else:
    print("Oops!  parsl done() call returned False!  For some reason we don't think we're done!")
