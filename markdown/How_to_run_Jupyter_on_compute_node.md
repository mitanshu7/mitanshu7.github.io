# How to run Jupyter on compute node

## Using [PBS](https://altair.com/pbs-professional) or not :)

**Mitanshu Sukhwani** • *07 June 2025*

# Prerequisites

1. Your python environment and required packages to be installed on your master node
  
2. Your ssh keys (of masternode) copied to the computes nodes. It's the default, unless you love `ssh-keygen`.
  

# Instructions

1. Open 2 Terminals (T1 & T2) on your local machine.
  
2. On T1 ssh into your master node by `ssh $USER:172.27.1.152` assuming `172.27.1.152` is the ip.

## Using PBS

3. Start an Interactive session using the `-I` flag. \
For example if you used the following PBS attributes in your batch script  
```bash
#PBS -l nodes=7:ppn=4
#PBS -l mem=2gb
#PBS -l walltime=15:00:00
#PBS -q default
``` 
The the command would translate to  
` $ qsub -I -X -q default -l select=7:ncpus=4,walltime=15:00:00,mem=2gb`
  
4. After you are assigned a node, proceed as follows

5. Activate your conda environment with the installed packages using `conda activate (envt-name)`  

6. Select a port number between *8000* and *9999*, this is where we will be exposing our jupyter environment. Lets pick **8546**

7. Start the Jupyter server using `jupyter-lab --no-browser --port 8546`

8. You will be shown a url of the nature, `http://localhost:8546/lab?token=XXXXXXXXXXXXXXXXXXXXX`. Make note of the url.

9. Open a second terminal on your local machine T2, no create a ssh tunnel (from local-machine to master-node) using,
  `ssh -L 8546:localhost:8546 $USER:172.27.1.152`

  
10. You are now logged into your masternode, now create a second ssh-tunnel (from master-node to compute-node) into that node using your already ssh'ed terminal T1 using:
  `ssh -L 8546:localhost:8546 $USER:10.10.10.1XX`
  
  where *$USER* your username, 
  and the ip address of nodes are `10.10.10.1XX` where `XX` is the node number.
  
11. Now you have a Jupyter server running on your allotted node and a ssh tunnel from local-machine $\to$ master-node $\to$ compute-node
  
12. Open your favorite web browser on your local machine and copy paste the above URL
  
13. Enjoy jupyter as if it was running locally ;)

### Caveats

1. You'll run into walltime
  
2. 2 ssh tunnels might slow down the speed. Cannot do a direct tunnel to compute node, since they are not available on the institute network.
  
3. Long wait times if you ask for ELongQ (168:00:00)


### Benefits

1. The resources are officially allotted and are yours to use for the time being.

## Bypassing PBS

3. After logging in your masternode, type and execute,
  `pbsnodes -a`
  This will give you information about all the nodes and their state.
  
4. Pick a free node, lets say it was *node05*.
  
5. Select a port number between *8000* and *9999*, this is where we will be exposing our jupyter environment. Lets pick **8546**
  
6. Now create a ssh-tunnel (from master-node to compute-node) into that node using your already ssh'ed terminal T1 using:
  `ssh -L 8546:localhost:8546 $USER:10.10.10.105`
  
  where *$USER* your username, 
  and the ip address of nodes are `10.10.10.1XX` where `XX` is the node number.
  
7. You are now logged in node05. You will see your conda envt already activated. now open jupyterlab/notebook using,
  `jupyter-lab --no-browser --port 8546`
  
8. you will be shown a url of the nature
  
  `http://localhost:8546/lab?token=XXXXXXXXXXXXXXXXXXXXX`
  
  Make note of the url.
  
9. Open a second terminal on your local machine T2, no create a ssh tunnel (from local-machine to master-node) using,
  `ssh -L 8546:localhost:8546 $USER:172.27.1.152`
  
10. Open your favorite web browser on your local machine and copy paste the above URL
  
11. Enjoy ;)

### Caveats

1. Although IT won't kill jobs on the compute node, they might.
  
2. 2 ssh tunnels might slow down the speed. Cannot do a direct tunnel to compute node, since they are not available on the institute network.
  
3. "Illegal" cause we haven't used the pbs scheduler
  
4. The compute nodes only seem to have 20GBs of ram and 40 cpus per node


### Benefits

1. No time limit. Scheduler takes a long time to assign you to ELongQ (even 2hrs is not enough of wait time), so bypasses that.