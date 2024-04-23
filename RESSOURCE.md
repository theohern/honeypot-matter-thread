# Ressources and commands to useful

## Homeassistant Supervisor
Follow the steps on this link https://github.com/home-assistant/supervised-installer \
First you need to install a os-agent, then you will be able to launch homassistant supervised. \
At the end of the installation you should see 7 containers up.

## Pivpn
Run the following command 
``` bash
curl -L https://install.pivpn.io | bash
```

## Fail2ban
First you need to install fail2ban 
``` bash
sudo apt install fail2ban
sudo systemctl restart fail2ban
sudo systemctl status fail2ban
```
You should see the service running.

Create a file /etc/fail2ban/jail.local with the content
```
[sshd]
enable = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 1
findtime = 300
bantime = 86400
```
Restart the service 
``` bash
sudo systemctl restart fail2ban
sudo systemctl status fail2ban
```
## Honeypot
Clone the github
``` bash
git clone https://github.com/theohern/honeypot-matter-thread.git 
```
Create a file /etc/systemd/system/honeypot.service with the content
```
[Unit]
Description=honeypot
After=network.target

[Service]
Type=simple
User=thernandez
ExecStart=/home/thernandez/honeypot-matter-thread/src/honeypot.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Follow step described in README.md

## WiFi in cli
List the able WiFi's 
``` bash
nmcli device wifi list
```

Connect to a specific WiFi 
``` bash
sudo nmcli device wifi connect <SSID> password <PASSWORD>
```

## Install Proxmox
Follow the steps of the following link : https://www.makeuseof.com/raspberry-pi-proxmox-virtualization-how-to-install/

## Put Haos on Proxmox
You can add homeasistant on proxmox via this command
``` bash
sudo -s
bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/vm/pimox-haos-vm.sh)"
```

## Configuration ssh
Go in the file /etc/ssh/sshd_config and find the cnofiguration 'AuthenticationPassword' set it to 'AuthenticationPassword no'. If this doesn't work, you will need to change the same configuration in the file /etc/ssh/sshd_config.d/*.conf

Create a new ssh key with PuttyGen and set a passphrase. Save the private key and paste the public key in the file ~/.ssh/authorized_keys

## First command for Debian

it will ask you first a usernam, enter 'root'. You will arrive in the root terminal. set up a password with the command 
``` bash
passwd
```
Then you will need to add a user
``` bash
adduser <USERNAME>
apt update && apt upgrade
apt install sudo
sudo usermod -aG sudo <USERNAME>
```
Log out and log in (rebbot is also a solution). Everything should be good after that

## Grafana
You can install grafana via the deb package 
``` bash
sudo apt-get install -y adduser libfontconfig1 musl
wget https://dl.grafana.com/enterprise/release/grafana-enterprise_10.4.2_arm64.deb
sudo dpkg -i grafana-enterprise_10.4.2_arm64.deb
```

You can check everythink is ok with the command
``` bash
sudo systemctl status grafana
```