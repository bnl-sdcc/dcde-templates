#!/bin/bash

#SBATCH -A dcde
#SBATCH -t 0:20:00
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -J relion-autopick
#SBATCH -p bdwall
#SBATCH -D /blues/gpfs/home/dcowley/sc19-out
#SBATCH -o relion-autopick.%j.out
#SBATCH -e relion-autopick.%j.err
#SBATCH --mail-user=david.cowley@pnnl.gov



export I_MPI_FABRICS=shm:tmi

#export PATH=$PATH:/home/ketan/dcde/relion/build/bin

export DATAROOT=/blues/gpfs/home/dcowley/sc19-demo
export OUTROOT=/blues/gpfs/home/dcowley/sc19-out
export JOBOUT=${OUTROOT}/AutoPick/job_${SLURM_JOBID}
export INSTAR=${DATAROOT}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${DATAROOT}/Select/job007/class_averages.star


#==========================
mkdir -p $JOBOUT || exit
cd $JOBOUT || exit
#cp /home/ketan/dcde/relion_benchmark/emd_2660.map . || exit
#ln -s /home/ketan/dcde/relion_benchmark/Particles ./Particles || exit
#FIXME:  straighten out dirctory mappings
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
FIXME:  Run this with singularity! ($HOME/relion_singv26.simg)
# Do we need a "-B /localmount:/containermount" argument?

singularity exec ${HOME}/relion_singv26.simg relion_autopick --i $INSTAR --ref $REFSTAR --odir $JOBOUT --pickname autopick --invert  --ctf  --ang 5 --shrink 0 --lowpass 20 --particle_diameter 200 --threshold 0.4 --min_distance 110 --max_stddev_noise 1.1 # --gpu "0"
touch run.stop
