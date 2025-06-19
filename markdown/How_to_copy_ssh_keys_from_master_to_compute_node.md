# How to copy ssh keys from master to compute node

## Fix when you run `ssh-keygen` on brand new HPC access

**Mitanshu Sukhwani** • _07 June 2025_

Learn more about HPC Architecture [here](https://phoenixnap.com/kb/hpc-architecture).

Generally, only the master node is connect to the internet, and the compute nodes are inter-connected with master node via a switch.

# Steps:

1. SSH into your master node.

2. Create new keys using `ssh-keygen`. No passphrase would be better for ease of access, but worse security.

3. Find the ip addresses of your (any) compute node from the `/etc/hosts/` file from masternode. We don't need to copy our ssh key to other nodes, as that happens itself.

4. Copy the public keys to compute nodes using `ssh-copy-id $USER@10.10.10.101`. Where `10.10.10.101` is the ip of your compute node.

5. Now you will be prompted to enter password for `$USER`, after that you can schedule your jobs using pbs.
