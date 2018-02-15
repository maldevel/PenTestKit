## Nikto

### Scanning an HTTPS target using a HTTP proxy

* Edit nikto.conf

```
nano /etc/nikto.conf
```

* Change line ```LW_SSL_ENGINE=auto``` to ```LW_SSL_ENGINE=SSLeay```

```
nikto -host example.com -port <port> -ssl -output nikto_https_report.html -useproxy http://127.0.0.1:8080
```
