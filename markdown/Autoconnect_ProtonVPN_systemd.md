---
# 1. Basic Identification
title: "Autoconnect to ProtonVPN using systemd"
subtitle: "**Why miss out on sweet protection?**"
author: "_Mitanshu Sukhwani_"
date: "`2026-08-15`"
lang: en
mainfont: 'Helvetica'

# 2. Metadata / SEO
description: "This blog post describes a method to autostart ProtonVPN client using the systemd service"
keywords: "protonvpn, vpn, security, autostart, systemd"
---

As much as the ProtonVPN is revered, I do not believe we have official support for auto connecting to the VPN on boot. Here is a simple way that uses systemd. 

The following has been tested on 'Fedora Linux 44 (Workstation Edition)', your mileage may vary.

# Get ProtonVPN CLI

Follow the instructions at the official [ProtonVPN Linux CLI](https://protonvpn.com/support/linux-cli) page. 

# Setup service

0. Create the systemd user config directory:

```bash
mkdir --parents ~/.config/systemd/user/
```

1. Create a service file using:

```bash
nano ~/.config/systemd/user/protonvpn.service
```

2. With the following contents:

```ini
[Unit]
Description=ProtonVPN
Wants=network-pre.target
After=network-pre.target NetworkManager.service systemd-resolved.service

[Service]
ExecStart=bash -c "/usr/bin/protonvpn disconnect && /usr/bin/protonvpn connect"

Restart=on-failure
RestartSec=30

StandardOutput=append:%h/protonvpn.log
StandardError=append:%h/protonvpn.log

[Install]
WantedBy=default.target
```

where `bash -c` reads the string and executes it, and `%h` redirects to `$HOME` variable.

Feel free to change the cli options in connect sub-command. I personally use `/usr/bin/protonvpn connect --securecore`.

3. Reload daemon, start & enable the service, and check the status:

```bash
systemctl --user daemon-reload
systemctl --user enable --now protonvpn.service
systemctl --user status protonvpn.service
```

This shall connect you to the VPN immediately. See logs for any troubleshooting using `cat ~/protonvpn.log`.

4. If you want to stop the ProtonVPN connection, use:

```bash
protonvpn disconnect
```

The regular `systemctl --user stop protonvpn.service` does not work here. I am yet to figure this part out.

5. If you want to refresh the connection, you may restart the service as usual:

```bash
systemctl --user restart protonvpn.service
```

Sometimes it'll take a minute as the cli is refreshing the server list in the background.

Cheers!