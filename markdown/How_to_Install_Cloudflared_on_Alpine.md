# How to Install [Cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) on [Alpine](https://www.alpinelinux.org/)

## For [Raspberri Pi Zero 2W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)

**Mitanshu Sukhwani** • _07 June 2025_

# Cloudflared Setup Guide

This guide will walk you through setting up Cloudflared on your system.

## Pre-Requisites

You need to have administrative (doas) access to your system.

Add nano editor using:

`doas apk update && doas apk add nano`

Here are the steps to install Cloudflared.

```bash
# Download the latest version of cloudflared, change `arm64` to `arm` at the end of the URL for 32-bit version.
doas wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O /usr/bin/cloudflared

# Give executable permissions to the downloaded file
doas chmod +x /usr/bin/cloudflared

# Check the version of cloudflared to confirm the installation
cloudflared -v
```

## Creating a Cloudflare Tunnel

After installing Cloudflared, you need to create a Cloudflare tunnel.

1.  Visit [https://one.dash.cloudflare.com](https://one.dash.cloudflare.com).

2.  Navigate to `Networks -> Tunnels -> Create a tunnel`.

3.  Fill in a name you like and save the tunnel.

4.  Find the code block below `After you have installed cloudflared on your machine, you can install a service to automatically run your tunnel whenever your machine starts:`.

5.  Replace `sudo` with `doas` before executing. Make note of the your `<TOKEN>` which comes after `sudo cloudflared service install`

## Starting the Cloudflared Service, while sustaining reboots

To automatically start the Cloudflared service on your machine, follow the steps below:

```bash
# Backup the original SysVinit file created by Cloudflared
doas mv /etc/init.d/cloudflared /etc/init.d/cloudflared.bak

# Create a new service file using:
doas nano /etc/init.d/cloudflared
```

With the following contents, replace `<TOKEN>` with the one noted above:

```bash
#!/sbin/openrc-run

name=$(basename $(readlink -f $0))

pidfile="/var/run/$name.pid"

command="/usr/bin/cloudflared"

command_args=" --pidfile /var/run/$name.pid  --autoupdate-freq 24h0m0s tunnel run --token <TOKEN>"

command_background=yes

stdout_log="/var/log/$name.log"

stderr_log="/var/log/$name.err"

depend() {
	need net
	after firewall
	use logger dns
}

```

Now, add the service file to OpenRC:

```bash
# Remove the service from the default runlevel (just in case it was added earlier)
doas rc-update del cloudflared

# Add the service to the default runlevel
doas rc-update add cloudflared default

# Start the service immediately
doas rc-service cloudflared start

```

That's it! You have successfully installed and set up Cloudflared on your system.

## Troubleshooting

If you encounter any issues while following this guide, please check the official [Cloudflared documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation) for further help.

Checkout OpenRC service init guide: https://github.com/OpenRC/openrc/blob/master/service-script-guide.md
