## stunnel Guide

### Installation

```bash
sudo apt-get install stunnel4
```

### Certificate

```bash
cd /etc/stunnel
openssl genrsa -out stunnel.key 2048
openssl req -new -key stunnel.key -out stunnel.csr
openssl x509 -req -days 365 -in stunnel.csr -signkey stunnel.key -out stunnel.crt
cat stunnel.crt stunnel.key > stunnel.pem
chmod 640 stunnel.key stunnel.pem
```

### Server

* Run stunnel in server mode, listening on port 44444 and forwarding traffic to Burp Pro on 127.0.0.1:8080.

```bash
cd /etc/stunnel
sudo nano server.conf
```

#### Contents

```
[stunnel-burp-server]
client = no
accept = 44444
connect = 8080
cert = /etc/stunnel/stunnel.pem
```

### Burp

* Set Burp on invisible mode(Proxy->Options->Proxy Listeners->Edit->Request handling->Check Support invisible proxying..) 
* Configure an upstream proxy server to forward all your traffic to 127.0.0.1 and port 22222.

### Client

* Run second stunnel in client mode, listening on port 22222 and forwarding all traffic to the IP address that corresponds to the target host.

```bash
cd /etc/stunnel
sudo nano client.conf
```

#### Contents

```
[stunnel-burp-client]
client = yes
accept = 127.0.0.1:22222
connect = target.ip.address:443
cert = /etc/stunnel/stunnel.pem
```


### Hosts file

* Add a hosts file entry for your target host to resolve to 127.0.0.1. 

```bash
sudo nano /etc/hosts
127.0.0.1       target.example.com
```

### Stunnel

```bash
stunnel4 /etc/stunnel/server.conf
stunnel4 /etc/stunnel/client.conf
```

#### Check if ports are opened

```bash
sudo netstat -plnt | grep 44444
sudo netstat -plnt | grep 22222
```

### Testing

* Now browse to https://target.example.com:44444
