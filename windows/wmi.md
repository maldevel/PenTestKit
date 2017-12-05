## Windows Management Instrumentation

### Get SID of a local user

```
wmic useraccount where name='username' get sid
```


### Get SID for current logged in user

```
wmic useraccount where name='%username%' get sid
```

### Get SID for current logged in domain user

```
whoami /user
```

### Get SID for the local administrator of the computer

```
wmic useraccount where (name='administrator' and domain='%computername%') get name,sid
```

### Get SID for the domain administrator

```
wmic useraccount where (name='administrator' and domain='%userdomain%') get name,sid
```

### Find username from a SID

```
wmic useraccount where sid='S-x-x-xx-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxx-xxxx' get name
```

