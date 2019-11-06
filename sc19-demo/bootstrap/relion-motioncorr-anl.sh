#!/bin/bash

#SBATCH -A dcde
#SBATCH -t 0:20:00
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -J relion-motioncorr
#SBATCH -p bdwall
#SBATCH -D /blues/gpfs/home/dcowley/relion-bootstrap
#SBATCH -o relion-motioncorr.%j.out
#SBATCH -e relion-motioncorr.%j.err
#SBATCH --mail-user=david.cowley@pnnl.gov



export I_MPI_FABRICS=shm:tmi


# NOTE: collapse all  file activity into DATAROOT.  I wanted to treat the relion
# tutorial  data dir as read-only but I don't think it likes that.

# Also I may need to start this entire process from the beginning to have the

export DATAROOT=/blues/gpfs/home/dcowley/relion-bootstrap
#export DATAROOT=/blues/gpfs/home/dcowley/sc19-data
#export DATAROOT=/blues/gpfs/home/dcowley/sc19-out
#export JOBOUT=${DATAROOT}/AutoPick/job_${SLURM_JOBID}
#mkdir -p $JOBOUT || exit

export INSTAR=${DATAROOT}/CtfFind/job003/micrographs_ctf.star
export CTFSTAR=${DATAROOT}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${DATAROOT}/Select/job007/class_averages.star
export COORDDIR=${DATAROOT}/AutoPick/job010/
export PARTSTAR=${DATAROOT}/Extract/job011/particles.star
export PARTDIR=${DATAROOT}/Extract/job011/
export MOVIESTAR=${DATAROOT}/Import/job001/movies.star
export MOTIONDIR=${DATAROOT}/MotionCorr/job002/

export MOTIONCOR_EXE=/usr/local/bin/MotionCor2_1.0.4 # I think this requires GPGPU!
export UNBLUR_EXE=/usr/local/bin/unblur_openmp_7_17_15.exe

# FIXED(?) If we go here, relion can't follow relative paths in its star files.
# So stick with default working directory set by SBATCH -D directive above.
#cd $JOBOUT || exit

echo -n "working directory: "
pwd

module load singularity/2.6.0

set -v

touch run.start

singularity exec  -B /blues/gpfs/home:/blues/gpfs/home ${HOME}/relion_singv26.simg relion_run_motioncorr --i $MOVIESTAR --o $MOTIONDIR --save_movies  --first_frame_sum 1 --last_frame_sum 16 --use_motioncor2 --bin_factor 1 --motioncor2_exe $MOTIONCOR_EXE --bfactor 150 --angpix 3.54 --patch_x 5 --patch_y 5 --dose_weighting --voltage 300 --dose_per_frame 1 --preexposure 0
# GPU required?
#--gpu "0"

touch run.stop
