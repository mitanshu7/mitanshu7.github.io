---
# 1. Basic Identification
title: "SSH into Your Android Phone Using Termux and Cloudflare Tunnels"
subtitle: "**Turn your Android device into a remotely accessible server**"
author: "_Mitanshu Sukhwani_"
date: "`2025-07-31`"
lang: en

# 2. Metadata / SEO
description-meta: "Learn how to set up secure SSH access to your Android device using Termux and Cloudflare Tunnels. Complete guide covering installation, configuration, and browser-based terminal access from anywhere in the world."
keywords: "termux, android, ssh, cloudflare tunnels, remote access, mobile server"
---

Ever wanted to SSH into your Android device from anywhere in the world? With Termux and Cloudflare Tunnels, you can turn your Android phone into a fully accessible remote server that you can connect to securely through your browser or terminal. This guide will walk you through the complete setup process.

## What You'll Need

- An Android device with [Termux](https://f-droid.org/packages/com.termux/) installed
- A Cloudflare account
- A domain managed by Cloudflare

## Step 1: Setting Up Cloudflared on Termux

First, let's install and configure Cloudflared on your Android device.

### Install Cloudflared

Open Termux and run:

```bash
pkg upgrade
pkg install cloudflared
```

### Create a Cloudflare Tunnel

1. Visit [https://one.dash.cloudflare.com](https://one.dash.cloudflare.com)
2. Navigate to `Networks -> Tunnels -> Create a tunnel`
3. Give your tunnel a memorable name and save it
4. Look for the section that says "OR run the tunnel manually in your current terminal session only"
5. Copy the `<TOKEN>` that appears after `cloudflared tunnel run --token`

### Set Up the Service

To ensure your tunnel runs reliably, we'll set it up as a service:

```bash
# Create logging directory
mkdir -p $PREFIX/var/service/cloudflared/log

# Symlink logger
ln -sf $PREFIX/share/termux-services/svlogger $PREFIX/var/service/cloudflared/log/run

# Create the service run file
nano $PREFIX/var/service/cloudflared/run
```

In the nano editor, paste the following content (replace `TOKEN` with your actual token):

```bash
#!/bin/bash
exec cloudflared tunnel run --token TOKEN
```

Make the file executable and start the service:

```bash
chmod +x $PREFIX/var/service/cloudflared/run
sv up cloudflared
sv-enable cloudflared
```

You can check if everything is working with:

```bash
sv status cloudflared
```

## Step 2: Configure SSH on Termux

Now let's set up the SSH server on your Android device.

### Install and Start SSH

```bash
pkg install openssh
sshd
sv up sshd
sv-enable sshd
```

### Find Your Username

You'll need this for connecting later:

```bash
whoami
```

The output will be something like `u0_a264`.

### Set Up Authentication

You have two options for authentication:

#### Option 1: Password Authentication

Set a password for your user:

```bash
passwd
```

#### Option 2: SSH Key Authentication (Recommended)

From your PC, copy your public key. If you don't have one, [generate a new SSH key first](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key).

```bash
# On your PC
cat .ssh/id_ed25519.pub
```

Copy the output, then in Termux:

```bash
nano .ssh/authorized_keys
```

Paste your public key and save the file.

## Step 3: Configure Cloudflare Access

Now we need to set up the public hostname and access policies.

### Create a Public Hostname

1. In your Cloudflare dashboard, create a new Public Hostname: `ssh.example.com` (replace with your domain)
2. Set the following properties:
   - Service type: `SSH`
   - URL: `127.0.0.1:8022`

### Set Up Access Control

1. Go to Cloudflare Access → Applications
2. Create a new application with these settings:
   - Application name: `ssh` (or any name you prefer)
   - Public hostname: `ssh.example.com`
   - Add an access policy to allow your email address
   - Browser rendering settings: `SSH`

## Step 4: Connect to Your Phone

You're now ready to SSH into your Android device!

### Via Browser

1. Visit `ssh.example.com` in your web browser
2. Authenticate using your email (as configured in Cloudflare Access)
3. Enter your Termux username (e.g., `u0_a264`)
4. Provide either your password or paste your private SSH key
5. You're in! You now have full terminal access to your Android device

## Making It Persistent

To ensure your tunnel starts automatically when your phone boots:

1. Install [Termux:Boot](https://wiki.termux.com/wiki/Termux:Boot) from F-Droid
2. Follow the setup instructions to enable the service on boot

## Troubleshooting

- If you need to stop the SSH service: `pkill sshd`
- Check tunnel status: `sv status cloudflared` or `sv status sshd`
- View tunnel logs: Check the log directory we created earlier

## Security Considerations

- Always use strong passwords or SSH keys
- Regularly update Termux packages with `pkg upgrade`
- Consider limiting access policies in Cloudflare to specific IP ranges if possible
- Monitor your tunnel usage through the Cloudflare dashboard

## Conclusion

You now have secure, remote access to your Android device from anywhere in the world! This setup is perfect for running scripts, managing files, or even using your phone as a lightweight server. The combination of Termux's Linux environment and Cloudflare's secure tunneling makes for a powerful and accessible mobile computing setup.

Happy remote computing!

## References

- [Termux Remote Access](https://wiki.termux.com/wiki/Remote_Access)
- [Cloudflare SSH Browser Rendering](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/use-cases/ssh/ssh-browser-rendering/)
- [Termux Services](https://wiki.termux.com/wiki/Termux-services)
- [Runit Runscripts](https://smarden.org/runit/runscripts)