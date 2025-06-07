# Stop podman containers from getting killed

## After logout/reboot


**Mitanshu Sukhwani** • *06 June 2025*


1.  Run the podman containers **without** a restart policy.
    
2.  Issue command:  

    `loginctl enable-linger $user`

> **WARNING**
>  systemd support is deprecated in podman, see [quadlets](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html). 

3.  Enable service using:  

    `podman generate systemd --files --name $container`,  

    where `$container` is your container id.
    
4.  In the service file, change
    
    ```bash
    [Install]
    WantedBy=multi-user.target
    ```

    to

    ```bash
    [Install]
    WantedBy=default.target
    ```

    if not done already by the generated service.

5.  We can copy the file to  

    `~/.config/systemd/user/container-foo.service`  

    If the directory doesnt exist,

    create it `mkdir -p ~/.config/systemd/user/`,

    copy the service file`cp container*service ~/.config/systemd/user/`,

    and then issue:  

    `systemctl --user daemon-reload`

6. Start a rootless container via  

    `systemctl --user start container-foo.service`

7. To persist reboots, also issue command:  

    `systemctl --user enable container-foo.service`

8. Stop a rootless container via  

    `systemctl --user stop container-foo.service`

Now the containers should live through the logout sessions (2) and reboots (7)


# References

1. [rootless systemd restarting containers when I log out of a shell](https://www.reddit.com/r/podman/comments/h00nfi/rootless_systemd_restarting_containers_when_i_log/)

2. [Running containers with Podman and shareable systemd services](https://www.redhat.com/sysadmin/podman-shareable-systemd-services)

3. [Why doesn't my systemd user unit start at boot?](https://unix.stackexchange.com/questions/251211/why-doesnt-my-systemd-user-unit-start-at-boot)


# Suggested reading

[Quadlet: Running Podman containers under systemd](https://mo8it.com/blog/quadlet/)