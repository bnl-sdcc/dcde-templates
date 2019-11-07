#!/bin/bash

#SBATCH -A dcde
#SBATCH -t 0:20:00
#SBATCH -N 1
#SBATCH --ntasks-per-node=36
#SBATCH -J relion-extract
#SBATCH -p bdwall
#SBATCH -D /blues/gpfs/home/dcowley/relion-bootstrap
#SBATCH -o relion-extract.%j.out
#SBATCH -e relion-extract.%j.err
#SBATCH --mail-user=david.cowley@pnnl.gov



export I_MPI_FABRICS=shm:tmi


export DATAROOT=/blues/gpfs/home/dcowley/relion-bootstrap

export INSTAR=${DATAROOT}/CtfFind/job003/micrographs_ctf.star
export CTFSTAR=${DATAROOT}/CtfFind/job003/micrographs_ctf.star
export REFSTAR=${DATAROOT}/Select/job007/class_averages.star
export COORDDIR=${DATAROOT}/AutoPick/job010/
export PARTSTAR=${DATAROOT}/Extract/job011/particles.star
export PARTDIR=${DATAROOT}/Extract/job011/

echo -n "working directory: "
pwd

module load singularity/2.6.0

set -v

touch run.start


singularity exec  -B /blues/gpfs/home:/blues/gpfs/home ${HOME}/relion_singv26.simg relion_preprocess --i $CTFSTAR --coord_dir $COORDDIR --coord_suffix _autopick.star --part_star $PARTSTAR --part_dir $PARTDIR --extract --extract_size 100 --norm --bg_radius 30 --white_dust -1 --black_dust -1 --invert_contrast

touch run.stop
