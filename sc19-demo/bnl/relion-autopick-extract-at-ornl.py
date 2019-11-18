parsl.clear()

#parsl.set_stream_logger()
parsl.load(ornl_config)
ornl_dfk = parsl.dfk()

@bash_app
def relion_autopick_extract_ornl(job_dir=None, stdout=None, stderr=None, mock=True):
    """
    Parameters
    ----------
    mock : (Bool)
       when mock=True
    """
    cmd_line = '''#!/bin/bash -l

export DATAROOT=/nfs/data/dcde-store/scratch/sc19-data
export RELION_SIMG=/nfs/sw/relion/relion_singv26.simg

export INSTAR=${{DATAROOT}}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${{DATAROOT}}/Select/job007/class_averages.star
export PICKDIR=${{DATAROOT}}/AutoPick/job010/
export PARTSTAR=${{DATAROOT}}/Extract/job011/particles.star
export PARTDIR=${{DATAROOT}}/job011/

echo -n "working directory: "
pwd
set -v

singularity exec -B ${{DATAROOT}}:${{DATAROOT}} ${{RELION_SIMG}} relion_autopick --i ${{INSTAR}} --ref ${{REFSTAR}} --odir ${{PICKDIR}} --pickname autopick --invert  --ctf  --ang 5 --shrink 0 --lowpass 20 --particle_diameter 200 --threshold 0.4 --min_distance 110 --max_stddev_noise 1.1 # --gpu "0"

echo ${{INSTAR}} > AutoPick/job010/coords_suffix_autopick.star

singularity exec -B ${{DATAROOT}}:${{DATAROOT}}  ${{RELION_SIMG}} relion_preprocess --i ${{INSTAR}} --coord_dir ${{PICKDIR}} --coord_suffix _autopick.star --part_star ${{PARTSTAR}} --part_dir ${{PARTDIR}} --extract --extract_size 100 --norm --bg_radius 30 --white_dust -1 --black_dust -1 --invert_contrast

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



relion_stdout=os.path.join(ornl_config.executors[0].working_dir, 'relion-ornl-extract.out')
relion_stderr=os.path.join(ornl_config.executors[0].working_dir, 'relion-ornl-extract.err')

local_logdir='/nfs/data/dcde-store/scratch/sc19-data/parsl-outputs'
local_logfile=os.path.join(local_logdir, 'relion-ornl-extract.out')

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

x = relion_autopick_extract_ornl(stdout=relion_stdout, stderr=relion_stderr, mock = True)
print('relion_autopick_extract_ornl() invoked, now waiting...')
x.result()
print('relion_autopick_extract_ornl() returned, should print output below:')

if x.done():
    with open(x.stdout, 'r') as f:
        print(f.read())
