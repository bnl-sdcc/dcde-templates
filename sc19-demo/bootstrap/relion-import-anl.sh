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


#export DATAROOT=/blues/gpfs/home/dcowley/sc19-data
export DATAROOT=/blues/gpfs/home/dcowley/relion-bootstrap
export OUTROOT=/blues/gpfs/home/dcowley/sc19-out
export JOBOUT=${OUTROOT}/AutoPick/job_${SLURM_JOBID}

export INSTAR=${DATAROOT}/CtfFind/job003/micrographs_ctf.star
export CTFSTAR=${DATAROOT}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${DATAROOT}/Select/job007/class_averages.star
export COORDDIR=${DATAROOT}/AutoPick/job010/
export PARTSTAR=${DATAROOT}/Extract/job011/particles.star
export PARTDIR=${DATAROOT}/Extract/job011/
export MOVIESTAR=${DATAROOT}/Import/job001/movies.star

mkdir -p $JOBOUT || exit
# FIXED(?) If we go here, relion can't follow relative paths in its star files.
# So stick with default working directory set by SBATCH -D directive above.
#cd $JOBOUT || exit

echo -n "working directory: "
pwd

module load singularity/2.6.0

set -v

touch run.start


singularity exec  -B /blues/gpfs/home:/blues/gpfs/home ${HOME}/relion_singv26.simg 'relion_star_loopheader rlnMicrographMovieName > $MOVIESTAR ; ls Micrographs/*.mrcs >> $MOVIESTAR'
touch run.stop
