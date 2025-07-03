---
# 1. Basic Identification
title: "How to change SSH Port on OCI"
subtitle: "**A tutorial**"
author: "_Mitanshu Sukhwani_"
date: "`2025-06-07`"
lang: en

# 2. Metadata / SEO
description: "Guide to securely change the SSH port on Oracle Cloud Infrastructure (OCI). Includes SELinux adjustments, firewall and security list updates, and troubleshooting via Cloud Shell."
keywords: "OCI, SSH, port change, SELinux, firewall, security list, Cloud Shell, Oracle Cloud Infrastructure"
---

# Steps

0. **NEEDED**: have a new user in sudo/wheel group with a password ready before doing anything here. It will be handy in troubleshooting via the [Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/devcloudshellgettingstarted.htm) in case things go awry. (Which is how this whole tutorial was executed :))

1. Back up the original config file:
   `sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak`

2. Run `sudo nano /etc/ssh/sshd_config` to edit the SSH config file.
   Replace `#Port 22` with `Port <port-number>`. Save the file, and do not restart the `sshd` service.

3. If you restart the sshd service, it'll show the error that selinux is preventing sshd from binding to new port. You now allow selinux using the command:

   `sudo semanage port -a -t ssh_port_t -p tcp <port-number>`

4. Now when you restart the sshd service, it should happen without any issues. However, you still will not be able to connect, just yet. So don't do it.

5. Now modiify firewall rules to allow the mentioned port.
   1. List firewall rules using: `sudo firewall-cmd --list-all`
   2. Add rule for the port: `sudo firewall-cmd --zone=public --permanent --add-port=<port-number>/tcp`
   3. Reload firewall: `sudo firewall-cmd --reload`
   4. List rules again to see changes: `sudo firewall-cmd --list-all`

6. Now go to https://cloud.oracle.com/compute/instances, Find your instance and go to the clickable subnet under primary vnic.

7. There select the default security list and add an ingress rule:
   1. Select Add Ingress rule
   2. In Source CIDR, enter `0.0.0.0/0` to allow every ip.
   3. Enter the `<port-number>` in Destination Port Range.

8. Restart the sshd service using: `sudo systemctl restart sshd`.

9. Voila!, now you can connect to your instance on a custom ssh port. Go on, try it!

10. You may delete ingress rule for port 22 once you can connect using the new port.

For more, see: [Eight ways to protect SSH access on your system | Enable Sysadmin](https://www.redhat.com/en/blog/eight-ways-secure-ssh)

# References:

1. [How to Update the Default SSH Port of Oracle Linux 8 in OCI](https://youtu.be/GL3FcUCkM_s)

2. [Oracle Linux 8: Configuring the Firewall](https://docs.oracle.com/en/operating-systems/oracle-linux/8/firewall/OL8-FIREWALL.pdf)

3. [Learn how to use SELinux.](https://docs.oracle.com/en/learn/ol-selinux/#selinux-booleans)
