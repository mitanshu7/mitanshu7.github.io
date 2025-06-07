# How to change SSH Port on OCI

## A tutorial

**Mitanshu Sukhwani** • *07 June 2025*

# Steps

0. **NEEDED**: have a new user in sudo group with a password handy before doing anything here. It will be handy in troubleshooting via the [Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/devcloudshellgettingstarted.htm) in case things go awry. (Which is how this whole tutorial was executed :)) 

1. Harden ssh using tips in [Eight ways to protect SSH access on your system | Enable Sysadmin](https://www.redhat.com/en/blog/eight-ways-secure-ssh)

2. If you restart the sshd service, it'll show the error that selinux is preventing sshd from binding to new port. Then you allow selinux using the command:

	`sudo semanage port -a -t ssh_port_t -p tcp <port-number>`

3. Now when you restart the sshd service using: `sudo systemctl restart sshd`, it should happen without any issues However you still will not be able to connect, just yet.

4. Now modiify firewall rules to allow the mentioned port. 

	1. List firewall rules using: `sudo firewall-cmd --list-all`
	2. Add rule for the port: `sudo firewall-cmd --zone=public --permanent --add-port=<port-number>/tcp`
	3. Reload firewall: `sudo firewall-cmd --reload`
	4. List rules again to see changes: `sudo firewall-cmd --list-all`

5. Now go to https://cloud.oracle.com/compute/instances, Find your instance and go to the clickable subnet under primary vnic.

6. There select the default security list and add an ingress rule:

	1. Select Add Ingress rule
	2. In Source CIDR, enter `0.0.0.0/0` to allow every ip.
	3. Enter the `<port-number>` in Destination Port Range.

7. Voila!, now you can connect to your instance on a custom ssh port.

8. Bonus, delete ingress rule for port 22. (YET TO TEST)


# References:

1. [How to Update the Default SSH Port of Oracle Linux 8 in OCI](https://youtu.be/GL3FcUCkM_s)

2. [Oracle Linux 8: Configuring the Firewall](https://docs.oracle.com/en/operating-systems/oracle-linux/8/firewall/OL8-FIREWALL.pdf)

3. [Learn how to use SELinux.](https://docs.oracle.com/en/learn/ol-selinux/#selinux-booleans)