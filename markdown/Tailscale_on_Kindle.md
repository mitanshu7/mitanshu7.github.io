# Tailscale on Kindle

## It's a rite of passage to run tailscale on weird devices.

**Mitanshu Sukhwani** • *08 June 2025*


Please visit [tailscale_kual](https://github.com/mitanshu7/tailscale_kual) for the appropriate code. 


## Prerequisites:

1. Jailbroken Kindle. ([see](https://kindlemodding.gitbook.io/kindlemodding))
2. KUAL installed. ([see](https://kindlemodding.gitbook.io/kindlemodding/post-jailbreak/installing-kual-mrpi))
3. [USBNetworking](https://wiki.mobileread.com/wiki/USBNetwork) hack installed and enabled. 
4. Set up [ssh keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) for ease of use.


## Usage:

1. Download the repository mentioned above.

2. Get the latest tailscale binaries for the `arm` architecture from [here](https://pkgs.tailscale.com/stable/#static). Or see releases page for a version that worked for me.

3. Place the `tailscale` and `tailscaled` binaries in the `tailscale/bin` folder of this (local) repository.

4. Place the tailscale folder into the `extensions` folder on your kindle.

5. In the KUAL menu, start `tailscaled` first then start `tailscale`.

6. You can find the url to login in the `extensions/tailscale` folder in `tailscale_start_log.txt` file, if this is a first time setup.

7. Copy the login url to a modern web browser and login using your preferred SSO.

8. After connecting the device should add the kindle to your `Machines` page on tailscale admin console. ([this](https://login.tailscale.com/admin/machines)).

9. Now you can see the (static) IP address assigned by Tailscale for your machine. You can use this ip to connect to kindle.

10. Note: Make sure the kindle screen is on, else the kindle sleeps the wifi. 

