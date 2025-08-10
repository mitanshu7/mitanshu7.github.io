---
# 1. Basic Identification
title: "How to run Tailscale without root"
subtitle: "**Longing to connect to your lab server?**"
author: "_Mitanshu Sukhwani_"
date: "`2025-06-07`"
lang: en

# 2. Metadata / SEO
description: "Learn how to set up and run Tailscale in user-space without root access. Includes steps for downloading static binaries, configuring tailscaled with a custom socket and port, automating startup via cron, and troubleshooting multi-user setups."
keywords: "Tailscale, user-space networking, tailscaled, cron job, Linux, static binaries, multi-user setup"
---

# Get tailscale
1. Fetch appropriate binaries for your architecture from here: [Tailscale Packages - stable track](https://pkgs.tailscale.com/stable/#static)

2. Untar using:

```bash
tar xvf tailscale_*.tgz
```

3. Rename folder:

```bash
mv tailscale_*/ tailscale/
```

4. Add folder to path & alias by appending the following lines in `~/.bashrc`:

```bash
export PATH="$HOME/tailscale:$PATH"
alias tailscale='tailscale --socket=$HOME/tailscale/tailscaled.sock'
```

## With Systemd (Recommended)

0. Create the systemd user config directory:

```bash
mkdir -p ~/.config/systemd/user/
```

1. Create a service file using:

```bash
nano ~/.config/systemd/user/tailscaled.service
```

2. With the following contents:

```ini
[Unit]
Description=Tailscale node agent
Documentation=https://tailscale.com/kb/
Wants=network-pre.target
After=network-pre.target NetworkManager.service systemd-resolved.service

[Service]
ExecStart=%h/tailscale/tailscaled --state=%h/tailscale/tailscaled.state --socket=%h/tailscale/tailscaled.sock -tun=userspace-networking --port=41641
ExecStopPost=%h/tailscale/tailscaled --cleanup

Restart=always
RestartSec=5

StandardOutput=append:%h/tailscale/tailscaled.log
StandardError=append:%h/tailscale/tailscaled.log

[Install]
WantedBy=default.target
```

`%h` redirects to `$HOME` variable.

3. Reload daemon, start & enable the service, and check the status:

```bash
systemctl --user daemon-reload
systemctl --user enable --now tailscaled.service
systemctl --user status tailscaled.service
```

4. Run the client with:

```bash
tailscale --socket=$HOME/tailscale/tailscaled.sock up
```

5. Log in and profit!

## Without Systemd (Hacky)

1. Create a bash script

```bash
nano $HOME/tailscale/start_tailscaled.sh
```

2. With the following contents:

```bash
#!/bin/bash

# Path to the tailscaled binary
TAILSCALED_START="$HOME/tailscale/tailscaled --state=$HOME/tailscale/tailscaled.state --socket=$HOME/tailscale/tailscaled.sock -tun=userspace-networking --port=41641"
TAILSCALED_CLEAN="$HOME/tailscale/tailscaled --cleanup"

# Function to check if tailscaled is running
is_running() {
    pgrep -x tailscaled > /dev/null
}

# Start tailscaled if not running
if ! is_running; then
    date
    echo "Starting tailscaled..."
    nohup $TAILSCALED_CLEAN >> $HOME/tailscale/tailscaled.log 2>&1 &
    nohup $TAILSCALED_START >> $HOME/tailscale/tailscaled.log 2>&1 &
else
    date
    echo "tailscaled is already running."
fi
```

4. Modify the crontab via
```bash
crontab -e
```

5. With

```bash
@reboot $HOME/tailscale/start_tailscaled.sh
* * * * * $HOME/tailscale/start_tailscaled.sh
```

5. Run tailscale using:

```bash
tailscale --socket=$HOME/tailscale/tailscaled.sock up
```

6. Login using the url shown and enjoy!

# Bonus:

If multiple people are using Tailscale without root, change to a free port and modify the following in your systemd.service/bash.script:

1. from

```bash
--port=41641
```

to
```bash
--port=41642
```

2. Only in bash script:

from

```bash
pgrep -x tailscaled
```

to

```bash
pgrep -f 41642
```
