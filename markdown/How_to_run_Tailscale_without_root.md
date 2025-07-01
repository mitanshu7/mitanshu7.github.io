---
title: "How to run Tailscale without root"
description: "Learn how to set up and run Tailscale in user-space without root access. Includes steps for downloading static binaries, configuring tailscaled with a custom socket and port, automating startup via cron, and troubleshooting multi-user setups."
---

## Longing to connect to your lab server?

**Mitanshu Sukhwani** • _07 June 2025_

# Steps:

Rename **mitanshu** to your **username**

1. Fetch appropriate binaries from here: https://pkgs.tailscale.com/stable/#static

2. Make them executible with:

   ```bash
   chmod +x /home/mitanshu/tailscale/tailscaled
   chmod +x /home/mitanshu/tailscale/tailscale
   ```

3. Create a bash script with `nano /home/mitanshu/tailscale/start_tailscaled.sh`:

   ```bash
   #!/bin/bash

   # Path to the tailscaled binary
   TAILSCALED_START="/home/mitanshu/tailscale/tailscaled --state=/home/mitanshu/.local/share/tailscale/tailscaled.state --socket=/home/mitanshu/tailscale/tailscaled.sock -tun userspace-networking --port=41641"
   TAILSCALED_CLEAN="/home/mitanshu/tailscale/tailscaled --cleanup"

   # Function to check if tailscaled is running
   is_running() {
       pgrep -x tailscaled > /dev/null
   }

   # Start tailscaled if not running
   if ! is_running; then
       date
       echo "Starting tailscaled..."
       nohup $TAILSCALED_CLEAN > /home/mitanshu/tailscale/tailscaled.log 2>&1 &
       nohup $TAILSCALED_START > /home/mitanshu/tailscale/tailscaled.log 2>&1 &
   else
       date
       echo "tailscaled is already running."
   fi
   ```

4. Add cronjob using:

   `crontab -e`

   and adding

   ```bash
   @reboot /home/mitanshu/tailscale/start_tailscaled.sh
   * * * * * /home/mitanshu/tailscale/start_tailscaled.sh
   ```

5. Run tailscale using:

   `tailscale --socket=/home/mitanshu/tailscale/tailscaled.sock up`

6. Login using the url shown and voila!

# Bonus:

If multiple people are using Tailscale, change to a free port and modify the following in your bash script:

1. from

`--port=41641`

to

`--port=41642`

2. from

`pgrep -x tailscaled`

to

`pgrep -f 41642`
