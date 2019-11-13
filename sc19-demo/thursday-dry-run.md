
# DCDE 11/13/19 dry run

## Topics
  * prerequisites
  * recipes, templates
  * lessons learned
  * components we're using
  * Participants
  * How accounts are created
  * Live demo


## Demo steps  

  - Prepare for demo
    - Log out all the things
    - Activate Globus endpoints
  - Demo begins
    - Log in to jupyterhub via cilogon
    - Talk about single DCDE identity used across sites, how they're set up for it
    - Talk about 3 sites participating - DCDE set up w/ oauth_ssh, Globus, mix of Condor & Slurm
    - Load demo page
    - Introduce Relion - say we're using containers, singlarity at each site
    - Show data set at bnl - say we've got it staged to other prerequisites
    - Talk about parsl -- we're leveraging it to run across a distributed,  mixed environment
    - Run import(?) at BNL.  
    - Sync data out to ORNL for (motioncorr or ctffind) -- something quick
    - Sync data back to BNL via Globus
    - Sync data out to ANL
    - Run autopick 3d refine(?) at  anl
    - pull data back to bnl
    - Show pictures w/ nglview at BNL

## list of steps/outputs:

| Target Site | job step | output type |  Output treatment | Approx. time|
| ----- | -----  | ----- | ----- | ---|
| ORNL |autopick | | | | |
| ORNL |extract | | | |
| ? | ctffind |  | | |
| ? | autopick |  | | |
| ANL | 3d refine? - view w/ NGL |   | | | 

##  Investigate (see sc19-screenply-cruft.md):

  * Did I do motioncor on Cascade w/ GPGPUs? I think I did.  
    * Is unblur in the singularity container?
  * Will relion_display work in any way?
  * Can we have some canned pictures?  Capture shots from X display or Chimera or something
