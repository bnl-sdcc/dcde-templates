#!/bin/bash

#SBATCH -A dcde
#SBATCH -t 0:20:00
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -J relion-autopick
#SBATCH -p bdwall
#SBATCH -D /blues/gpfs/home/dcowley/sc19-data
#SBATCH -o relion-autopick.%j.out
#SBATCH -e relion-autopick.%j.err
#SBATCH --mail-user=david.cowley@pnnl.gov



export I_MPI_FABRICS=shm:tmi


export DATAROOT=/blues/gpfs/home/dcowley/sc19-data
export OUTROOT=/blues/gpfs/home/dcowley/sc19-out
export JOBOUT=${OUTROOT}/AutoPick/job_${SLURM_JOBID}

export INSTAR=${DATAROOT}/CtfFind/job003/micrographs_ctf.star
export CTFSTAR=${DATAROOT}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${DATAROOT}/Select/job007/class_averages.star
export COORDDIR=${DATAROOT}/AutoPick/job010/
export PARTSTAR=${DATAROOT}/Extract/job011/particles.star
export PARTDIR=${DATAROOT}/Extract/job011/

mkdir -p $JOBOUT || exit
# FIXED(?) If we go here, relion can't follow relative paths in its star files.
# So stick with default working directory set by SBATCH -D directive above.
#cd $JOBOUT || exit

echo -n "working directory: "
pwd

module load singularity/2.6.0

set -v

touch run.start


# autopick step from relion 2.1 tutorial:
# Do we need a "-B /localmount:/containermount" argument?

singularity exec  -B /blues/gpfs/home:/blues/gpfs/home ${HOME}/relion_singv26.simg relion_preprocess --i $CTFSTAR --coord_dir $COORDDIR --coord_suffix _autopick.star --part_star $PARTSTAR --part_dir $PARTDIR --extract --extract_size 100 --norm --bg_radius 30 --white_dust -1 --black_dust -1 --invert_contrast

#relion_autopick --i $INSTAR --ref $REFSTAR --odir $JOBOUT --pickname autopick --invert  --ctf  --ang 5 --shrink 0 --lowpass 20 --particle_diameter 200 --threshold 0.4 --min_distance 110 --max_stddev_noise 1.1 # --gpu "0"
touch run.stop
