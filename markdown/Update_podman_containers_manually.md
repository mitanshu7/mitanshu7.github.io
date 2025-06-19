# Update podman containers manually

## When I couldn't figure out [auto-update](https://docs.podman.io/en/latest/markdown/podman-auto-update.1.html)

**Mitanshu Sukhwani** • _06 June 2025_

1. Stop running containers using:

   `podman stop CONTAINER_ID`

   or using

   `systemctl --user stop container-CONTAINER_NAME.service`

   if systemd service is generated and running.

2. Fetch the latest image:

   `podman pull CONTAINER_NAME:TAG`

3. Start the container via the original command that you used to start the very first time, modify the tag if needed.

4. Generate new service file using the following command:

   `podman generate systemd --new CONTAINER_NAME > ~/.config/systemd/user/container-CONTAINER_NAME.service`

5. Reload services:

   `systemctl --user daemon-reload`

6. To persist reboots, also issue command:

   `systemctl --user enable container-CONTAINER_NAME.service`
