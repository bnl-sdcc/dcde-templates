#!/bin/bash -l

echo "****************************************"
set -v
date
whoami
id
hostname
which singularity
date

echo -n "initial directory:"
pwd
echo -n "contents:"
ls
echo -n "HOME = "
echo $HOME

#export HOME=/direct/usatlas+grid/dcde1000006
#export HOME=/usatlas/grid/dcde1000006
export HOME=/sdcc/u/dcde1000006
#env
echo "contents of $HOME:"
ls -l $HOME

DATAROOT=${HOME}/relion-tut/relion21_tutorial/PrecalculatedResults
echo "\$DATAROOT: $DATAROOT"
#ls $DATAROOT

mkdir -p PostProcess/$$/postprocess || exit
#ln -s ${DATAROOT}/MaskCreate MaskCreate
#ln -s ${DATAROOT}/Refine3D Refine3D

echo -n "working directory:"
pwd
echo -n "contents:"
ls


#singularity exec ${HOME}/relion_singv26.simg /usr/local/bin/relion_postprocess --mask ${DATAROOT}/MaskCreate/first3dref_th002_ext2_edg3/mask.mrc --i ${DATAROOT}/Refine3D/after_first_class3d/run --o PostProcess/$$/postprocess  --angpix 3.54 --mtf ${DATAROOT}/mtf_falcon2_300kV.star --auto_bfac  --autob_lowres 10
singularity exec ${HOME}/relion_singv26.simg /usr/local/bin/relion_postprocess --mask ${DATAROOT}/MaskCreate/first3dref_th002_ext2_edg3/mask.mrc --i ${DATAROOT}/Refine3D/after_first_class3d/run  --angpix 3.54 --mtf ${DATAROOT}/mtf_falcon2_300kV.star --auto_bfac  --autob_lowres 10

pwd

set +v

ls -l

date

echo "****************************************"
