## Socat Guide

### Tunnel a connection from a local TCP port to a remote service
```bash
socat -v tcp4-listen:8181,reuseaddr,fork tcp4:x.x.x.x:80
```

### Tunnel a plain text connection to an SSL endpoint
```bash
socat -v tcp4-listen:8181,reuseaddr,fork ssl:x.x.x.x:443,verify=0
```

**Enable the use of a client side certificate (authentication)**
```bash
socat -v tcp4-listen:9000,reuseaddr,fork ssl:x.x.x.x:443,verify=0,cert=./mycert.pem
```

### Man in the middle an SSL connection

**Diagram**
```
Application ==SSL==> socat #1 —plain-text—> socat #2 ==SSL==> Remote service
```

**Shell 1**
```bash
socat -v tcp4-listen:8181,reuseaddr,fork ssl:x.x.x.x:443,verify=0
```

**Shell 2**
```bash
socat -v openssl-listen:8282,cert=cert.pem,verify=0,reuseaddr,fork
tcp4:localhost:8181
```

### Modify HTTP traffic in transit to disable gzip/deflage encodings

**Diagram**
```
Application ==SSL==> socat #1 —plain-text—> netsed —plain-text—> socat #2 ==SSL==> Remote service
```

**Shell 1**
```bash
socat -v tcp4-listen:8181,reuseaddr,fork ssl:x.x.x.x:443,verify=0
```

**Shell 2**
```bash
netsed tcp 8282 127.0.0.1 8181 ‘s/gzip/ ‘ ‘s/deflate/ ‘
```

**Shell 3**
```bash
socat -v openssl-listen:8383,cert=cert.pem,verify=0,reuseaddr,fork
tcp4:localhost:8282
```

