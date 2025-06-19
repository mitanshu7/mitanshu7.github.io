# Setup [Nebula](https://nebula.defined.net/docs/)

## The Open-Source [Tailscale](https://tailscale.com/) Alternative

**Mitanshu Sukhwani** • _19 June 2025_

Traditionally, VPNs have had a hub-and-spoke architecture. There are multiple clients, who want to talk to multiple servers. You would then setup a designated server as the VPN server. This server can access both, the internet and your office network, which is how you can _relay_ your `ssh` connections to the destination.

![Hub-and-Spoke VPN. Source: [Tailscale](https://tailscale.com/blog/how-tailscale-works)](https://cdn.sanity.io/images/w77i7m8x/production/3cbc3fa27f0b798d3a0bc98f57829a9083dad769-1400x1080.svg?w=3840&q=75&fit=clip&auto=format)

However, there is a single point of failure with this model, and latency can take a huge hit if both the machines are geographically closer but the hub is in some far-away land.

![Latency hits. Source: [Tailscale](https://tailscale.com/blog/how-tailscale-works)](https://cdn.sanity.io/images/w77i7m8x/production/d0363ebfb736fa6e394aef3cb26585cecd842cd2-1320x980.svg?w=3840&q=75&fit=clip&auto=format)

Thus, newer generation of VPNs solve this by using a mesh network. Where every machine (node) is connected to every other node (machine).

![Mesh network. Source: [Tailscale](https://tailscale.com/blog/how-tailscale-works)](https://cdn.sanity.io/images/w77i7m8x/production/e989a4a69acd182abbd662d0de93cb31c4c4d210-1600x1080.svg?w=3840&q=75&fit=clip&auto=format)

But how do the clients know with whom to talk to? That is handled by a Coordination Server (closed-source), which is essentially a dropbox to exchange public keys.

![Coordination Server. Source: [Tailscale](https://tailscale.com/blog/how-tailscale-works)](https://cdn.sanity.io/images/w77i7m8x/production/dbba97845c1ad1955669cc6a84c94f9d5fb78ade-1600x1080.svg?w=3840&q=75&fit=clip&auto=format)

This looks like a Hub and Spoke model again, but its only the keys that are transferred through this server, the data plane remains the mesh.

There are some NAT punching tricks that help with traversal and firewalls, which is beautifully explained in this blogpost by Tailscale: [How NAT traversal works](https://tailscale.com/blog/how-nat-traversal-works).

Tailscale makes this setup very convenient, all you have to do is install the app (which is open-source) and sign in using your available [SSO](https://en.wikipedia.org/wiki/Single_sign-on) (gmail/microsoft/github/apple/email). This is what I would recommend if you are new to networking or want a hands-off approach. Here is a detailed comparison between [Nebula vs. Tailscale](https://tailscale.com/compare/nebula).

[Nebula](https://github.com/slackhq/nebula) has all of it's components open-source, which gives you the peace of mind when it comes to trusting your networking. Nebula, as listed on their [quick-start](https://nebula.defined.net/docs/guides/quick-start/) page, has the following components:

1. Lighthouse - similar to the coordination server above, it helps find other hosts on the network.
2. Hosts - any device added to the Nebula network.
3. Certificate Authority - a trusted entity that issues and manages digital certificates.

Now, nebula assumes we already have a Lighthouse setup with a public facing ip. Let's get that sorted. On the github page they recommend a $6/month digital ocean vm, but I don't have that kind of money so we'll look for free things. [Google compute](https://cloud.google.com/free/docs/free-cloud-features#compute) has a free tier which gives you a e2-micro VM. This is more than enough for our task.

After [signing up](https://console.cloud.google.com/getting-started?pli=1) for an account, spin up a VM using: [Create and start a Compute Engine instance](https://cloud.google.com/compute/docs/instances/create-start-instance). I used a Debian 12 image for light ram usage, and make sure to change the disk type to `standard persistent disk` to not incur any charges.

After the VM spins up, login to your instance using [gcloud-cli](https://cloud.google.com/sdk/docs/install-sdk):

```bash
gcloud compute ssh --zone "zone_name" "instance_name" --project "project_name"
```

You may want to run `sudo apt update && sudo apt upgrade -y` to update your VM install. Since Google thresholds your usage, this will take a long time to complete, so you may want to grab some coffee while this finishes.
