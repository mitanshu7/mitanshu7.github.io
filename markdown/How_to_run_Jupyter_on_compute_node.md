# How to run Jupyter on compute node

## Using [PBS](https://altair.com/pbs-professional) or not :)

### For IISER Tirupati HPC, should work elsewhere with little modifications

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

9. Open a second terminal on your local machine T2, no create a ssh tunnel (from local-machine to master-node) using:

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
  
2. ssh tunnels might slow down the speed. Cannot do a direct tunnel to compute node, since they are not available on the institute network.
  
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
  
7. You are now logged in node05. You will see your conda envt already activated. now open jupyterlab/notebook using:

  `jupyter-lab --no-browser --port 8546`
  
8. you will be shown a url of the nature
  
  `http://localhost:8546/lab?token=XXXXXXXXXXXXXXXXXXXXX`
  
  Make note of the url.
  
9. Open a second terminal on your local machine T2, no create a ssh tunnel (from local-machine to master-node) using:

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

# Bonus

## Bash scripts to bypassing PBS

1. Create a file titled `sshtunneltohpc.sh` with the following contents:

  ```bash
  #!/bin/bash

  #Different gobal variables
  myport=8781 #choose between 8000 and 9999
  iam=$(whoami) #your username to login into masternode/hpc
  masterpass= #your pass
  loginip=172.27.1.152 #masternode ip address

  # Connecting to masternode by using pass
  sshpass -p $masterpass ssh -o StrictHostKeyChecking=no -L $myport:localhost:$myport $iam@$loginip "bash sshtunneltonode.sh"

  # Connecting to masternode by using keys
  #ssh -L $myport:localhost:$myport $iam@$loginip "bash sshtunneltonode.sh"
  ```

2. Create a file titled `sshtunneltonode.sh` with the following contents:

  ```bash
  #!/bin/bash

  #Different gobal variables
  myport=8781 #choose between 8000 and 9999
  iam=$(whoami) #your username to login into masternode/hpc

  # grabbing the first free node
  firstfreenode=$(pbsnodes -a | grep -i "free" -n | cut -d ":" -f 1 | sed -n '1p')

  #finding node number
  if [ $firstfreenode = 4 ]
  then
      node=01
  elif [ $firstfreenode = 26 ]
  then
      node=02
  elif [ $firstfreenode = 48 ]
  then
      node=03
  elif [ $firstfreenode = 70 ]
  then
      node=04
  elif [ $firstfreenode = 92 ]
  then
      node=05
  elif [ $firstfreenode = 114 ]
  then
      node=06
  elif [ $firstfreenode = 136 ]
  then
      node=07
  elif [ $firstfreenode = 158 ]
  then
      node=08
  elif [ $firstfreenode = 180 ]
  then
      node=09
  elif [ $firstfreenode = 202 ]
  then
      node=10
  elif [ $firstfreenode = 224 ]
  then
      node=11
  elif [ $firstfreenode = 245 ]
  then
      node=12
  elif [ $firstfreenode = 266 ]
  then
      node=13
  else
      node=14
  fi

  #assiging ip
  nodeip=10.10.10.1$node #ip address of compute node
  #echo $nodeip

  # sshing into selected compute node
  ssh -L $myport:localhost:$myport $iam@$nodeip "bash start-jupyter.sh"
  ```

3. Create a file titled `start-jupyter.sh` with the following contents:

  ```bash
  myport=8781
  export NUMEXPR_MAX_THREADS=40
  jupyter-lab --no-browser --port=$myport
  ```

4. Keep the file `sshtunneltohpc.sh` on your local machine and edit the `masterpass=` parameter accordingly. if you have the keys setup, comment lines accordingly to avoid exposing the pass.

5. Copy the files `sshtunneltonode.sh` and `start-jupyter.sh` to your masternode.

6. Go to the terminal of your local machine and just run ```bash sshtunneltohpc.sh```

7. This will connect your local machine to hpc, and then execute the `sshtunneltonode.sh` script automatically.

8. The `sshtunneltonode.sh` script will connect to the first **"free"** node and execute `start-jupyter.sh` automatically.

9. You'll be shown a url at the end, just open that and you'll be connected to compute node running your instance of Jupyterlab

