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
export REFSTAR=${DATAROOT}/Select/job007/class_averages.star

mkdir -p $JOBOUT || exit
# FIXED(?) If we go here, relion can't follow relative paths in its star files.
# So stick with default working directory set by SBATCH -D directive above.
#cd $JOBOUT || exit

echo -n "working directory: "
pwd

#=========================
# OLD STUFF:
#export PATH=$PATH:/home/ketan/dcde/relion/build/bin
#cp /home/ketan/dcde/relion_benchmark/emd_2660.map . || exit
#ln -s /home/ketan/dcde/relion_benchmark/Particles ./Particles || exit
#mkdir -p  $SLURM_SUBMIT_DIR/class3d || exit
#ln -s ${DATAROOT}/Extract Extract || exit
#=========================

module load singularity/2.6.0

#echo
#echo "printenv output:"
#echo
#printenv
## Echo the runtime libraries that your executable is linked to
## A "not found" message here says your build environment is different
## than your runtime environment.
##
#echo
#echo "ldd -r output:"
#echo
#ldd -r `which relion_refine_mpi`

set -v

touch run.start


# autopick step from relion 2.1 tutorial:
# Do we need a "-B /localmount:/containermount" argument?

singularity exec  -B /blues/gpfs/home:/blues/gpfs/home ${HOME}/relion_singv26.simg relion_autopick --i $INSTAR --ref $REFSTAR --odir $JOBOUT --pickname autopick --invert  --ctf  --ang 5 --shrink 0 --lowpass 20 --particle_diameter 200 --threshold 0.4 --min_distance 110 --max_stddev_noise 1.1 # --gpu "0"
touch run.stop
