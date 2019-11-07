#!/bin/bash

#SBATCH -A dcde
#SBATCH -t 0:20:00
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -J relion-autopick
#SBATCH -p bdwall
#SBATCH -D /blues/gpfs/home/dcowley/relion-bootstrap
#SBATCH -o relion-autopick.%j.out
#SBATCH -e relion-autopick.%j.err
#SBATCH --mail-user=david.cowley@pnnl.gov



export I_MPI_FABRICS=shm:tmi


export DATAROOT=/blues/gpfs/home/dcowley/relion-bootstrap

export INSTAR=${DATAROOT}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${DATAROOT}/Select/job007/class_averages.star
export PICKDIR=${DATAROOT}/AutoPick/job010/


echo -n "working directory: "
pwd

module load singularity/2.6.0

set -v

touch run.start

singularity exec  -B /blues/gpfs/home:/blues/gpfs/home ${HOME}/relion_singv26.simg relion_autopick --i $INSTAR --ref $REFSTAR --odir $PICKDIR --pickname autopick --invert  --ctf  --ang 5 --shrink 0 --lowpass 20 --particle_diameter 200 --threshold 0.4 --min_distance 110 --max_stddev_noise 1.1 # --gpu "0"
touch run.stop
