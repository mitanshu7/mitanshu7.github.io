---
# 1. Basic Identification
title: "How to register (any*) passkey to linux?"
subtitle: "**Sudo swish**"
author: "_Mitanshu Sukhwani_"
date: "`2026-10-16`"
lang: en
mainfont: "Helvetica"

# 2. Metadata / SEO
description: "Register a new device on linux using command line and authenticate with a touch."
keywords: "passkey, security, security key, linux, pam, auth,"
---

# Prerequisites

1. A FIDO2 complaint security key. \*_Aren't most of them nowadays?_ I have [Ensurity Auth Touch](https://icons.net.in/product/thinc-auth-touch/).
2. A root shell. Keep this safe untill you are sure everything works. I still have one open (just in case).

# Recipe

0. Plug in the security device. Create a root shell and keep it safe:

```bash
sudo su root
```

1. Install the `pam-u2f` package:

```bash
# Ubuntu
sudo apt-get install libpam-u2f pamu2fcfg

# Fedora
sudo dnf install pam-u2f pamu2fcfg
```

2. `pamu2fcfg` helps you create the configuration for the U2F PAM module. Let's create one:

```bash
# Basic, only checks presence of a user
pamu2fcfg

# Checks user presence with PIN too
pamu2fcfg --pin-verification
```

Add the `--resident` flag in case you want to store the configuration **on device**. Beware that these slots are limited and depend on your manufacturer.

3. If you have a key which takes in human touch to confim presence, you will need to touch the sensor after executing either of the above commands. This will print the PAM configuration, it should look like this:

```bash
# This is the PIN variant
mitanshu:Ph6+58Ttduz9D5z67SVtitg...zWzyi42I85Bw==,es256,+presence+pin
```

4. Now let's save this configuration to a file.

```bash
# Paste the config in this file
sudo nano /etc/u2f_mappings
```

5. Update the PAM auth config to now take this method

```bash
# Drop into a root shell
sudo su root

# Open the config file
nano /etc/pam.d/common-auth

# Paste the following, making sure it is above the line that contains `pam_unix.so`.
auth required pam_u2f.so authfile=/etc/u2f_mappings cue pinverification=1
```

In `required` mode, the key will be used and required for 2FA. Change it to `sufficient` in case you also want to use password alone.

You can turn off being asked for pin by setting `pinverification=0`. However it will not turn off pin if you chose to create the config with `--pin-verification` above.

6. Open a new shell and test:

```bash
su mitanshu
```

Touch the key, enter pin if needed. If the command succeeds, you key is now set.

Double check the expected usage before removing the root shell.

# Reference

1. [pamu2fcfg](https://man.archlinux.org/man/pamu2fcfg.1)
2. [pam.conf](https://man.archlinux.org/man/pam.conf.5)
3. [pam-u2f](https://developers.yubico.com/pam-u2f)
4. [FIDO2 security key sign-in on Linux](fido_security_key_medium_blog.html)
5. [libfido2](https://developers.yubico.com/libfido2/)
