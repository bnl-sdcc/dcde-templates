# DCDE Relion demo screenplay


## Planned SC19 DCDE PARSL demo

### Topics
  * prerequisites
  * recipes, templates
  * lessons learned
  * components we're using
  * Participants
  * How accounts are created
  * Live demo

### The setup

This is will be a live demo to be performed at the Department of Energy Exhibition booth at the Supercomputing 2019 conference.  The demo will  feature the DCDE single sign-on scheme, with Jupyter notebooks and PARSL middleware being used to access remote HPC resources

### The players
The client and controlling machine will be `jupyter05.sdcc.bnl.gov`.  
  * Jupyter notebook pages will:
    * Transfer Data to and from compute clusters and/or Globus endpoints (Globus or oauth-ssh SCP)
    * Submit batch jobs to compute clusters
    * Visualize output data from the batch jobs
  * Compute resources:  
    * Argonne cluster:  via `gsissh.lcrc.anl.gov`
    * Brookhaven Cluster via  `spce01.sdcc.bnl.gov`
    * ORNL Cluster via `dcde-ext.ornl.gov`
  * Globus endpoints:
    * `mscdtn.emsl.pnl.gov`?
    * `globus02.sdcc.bnl.gov`
  * Applications
    * `Relion` run in batch jobs on the DCDE compute resources
    * `Singularity`
    * `Globus` to sync directories between compute resources
    * `Nglview` to visualize results in the jupyter notebook page.
    * ~~Chimera (/Applications/Chimera.app/Contents/MacOS/chimera)~~

### Preparatory work
  * Verify oauth-ssh works (refer to https://github.com/bnl-sdcc/dcde-templates/tree/master/site-tests) from jupyter05 to:
    * spce01.sdcc.bnl.gov
    * gssh.lcrc.anl.gov
    * dcde-ext.ornl.gov
    * dcde.lbl.gov
  * Verify PARSL on each compute resource can:
     1. Run a `uname`- style command on a batch node and return output to the parsl client on `jupyter05`    
     2. Run a trivial relion job in a singularity container and return output to the parsl client on `jupyter05`    
  * Verify Globus transfer operations work between endpoints at:
    * ANL <-> BNL
    * ORNL <-> BNL
    * LBNL <-> BNL?
  * Install `nglview` (https://github.com/arose/nglview) on `jupyter05`
  * Pre-stage input data (Relion tutorial data set) to all participating compute site
  * Make sure reservations are avaiable on compute resources for immediate job turnaround

### Demo Steps:

  1. Log into `jupyter05.sdcc.bnl.gov` with DCDE account
  1. Submit Job A to Lab A
  1. Sync output of Job A back to jupyter05
  1. Visualize output of Job A on Jupyter05
  1. Sync new data from job A out to Lab B (input to next job)
  1. Submit Job B to Lab B
  1. Sync output of Job B back to jupyter05
  1. Visualize output of job B on Jupyter05
  1. Sync new data from job B out to Lab C (input to next job)
  1. Submit Job C to Lab C
  1. Sync output of Job C back to jupyter05
  1. Visualize output of job C on Jupyter05


### About the computing

Cryo-Electron Microscopy is an experimental technique that can be used to determine atomic structure of biomolecules such as proteins.  The molecules are suspended in water and flash frozen into amorphous ice.  Then they are imaged with transmission electron Microscopy.  The data sets can be very large (multiple terabytes) and require extensive processing to construct 3D models of the molecule(s) present in the sample.

We use the relion application, which can be run on many different types of compute platforms, including HPC clusters and GPGPU-based machines.  We will see a few computational steps of a multi-step  pipeline demonstrated today

# April demo steps:

## Run 3D Classification at ANL:

```
[dcowley@beboplogin5 ~]$ sbatch < run-3d-class-dcde.sbatch ; watch showq -u dcowley

[dcowley@beboplogin5 875970]$ squeue -u dcowley
JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
876982    bdwall relion-3  dcowley  R       0:19      4 bdw-[0161-0164]

[dcowley@beboplogin5 dcde]$ tail -f  relion-3d-refine.876982.bdw-0161.out
```

## While  Argonne job runs

### show input movie frames on cascade

`relion_display --i  Micrographs/Falcon_2012_06_12-14_57_34_0_movie.mrcs ``


### Show particles from 2D classification(?)  on Cascade


```
relion_display  --i Select/after_sorting/particles.star
```


## Pull data back from ANL:
```
[dcde@d2abd7b78f83 ~]$ ./scripts/anl-pull.sh
```

## Show files from  
  * Cascade:  `relion_display --i  Class3D/first_exhaustive/run_it004_class00?.mrc`
  * ANL run: `<chimera> dcde-relion-demo/3dClassify/dcde/875970/*.mrc`

## Run (something) at ORNL if they become live:

## Run PostProcessing at BNL:

```
Wed Jan 30 18:04:40 EST 2019
-bash-4.2$
-bash-4.2$ cd ~/dcde-relion-demo/PostProcess/
-bash-4.2$ pwd
/usatlas/grid/dcde1000006/dcde-relion-demo/PostProcess
-bash-4.2$ condor_submit ~/relion-bnl-demo.jdl ; watch condor_q
```

## Pull bnl files back via rsync:

```
[dcde@fac9eee44f32 ~]$ scripts/bnl-pull.sh
~/dcde-relion-demo ~
receiving incremental file list
./
```

## Show files from BNL in Chimera

 `/Applications/Chimera.app/Contents/MacOS/chimera dcde-relion-demo/3dClassify/dcde/875970/class3d_it004_class002.mrc`
