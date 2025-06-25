#!/bin/bash
#|
#| > Install and run a connector
#| To connect your tunnel to Cloudflare, copy-paste one of the following commands into a terminal window. Remotely managed tunnels require that you install cloudflared 2022.03.04 or later.
#| If you don’t have cloudflared installed on your machine:
#| get the token at -> https://one.dash.cloudflare.com/1d2505ce8bda0a19b128ae074c38ee1a/networks/tunnels/cfd_tunnel/a84ab30c-922c-4127-be3a-92c3db75038b/edit?tab=overview
CLOUDFLARE_TUNNEL_TOKEN="[YOUR_CLOUDFLARE_TUNNEL_TOKEN]"

# Add cloudflare gpg key
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null

# Add this repo to your apt repositories
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | sudo tee /etc/apt/sources.list.d/cloudflared.list

# install cloudflared
sudo apt-get update && sudo apt-get install cloudflared

# After you have installed cloudflared on your machine, you can install a service to automatically run your tunnel whenever your machine starts:
sudo cloudflared service install $CLOUDFLARE_TUNNEL_TOKEN
# OR run the tunnel manually in your current terminal session only:
cloudflared tunnel run --token $CLOUDFLARE_TUNNEL_TOKEN

# To enable the cloudflared service to start on boot:
sudo systemctl enable cloudflared

# To check the status of the cloudflared service:
sudo systemctl status cloudflared

# To check the status of your tunnel, run:
sudo journalctl -u cloudflared -f

#| Tips:
#| - explore https://tteck.github.io/Proxmox/#cloudflared-lxc to learn how to run cloudflared in a container.
#| - explore https://github.com/tteck/Proxmox/blob/main/ct/cloudflared.sh to learn how to run cloudflared in a container.