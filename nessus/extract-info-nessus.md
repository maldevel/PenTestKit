## Nessus Information

* Export Scan results as a csv file.

### Export Critical Vulnerabilities

```bash
cat myproject.csv | grep '"Critical"' | sed 's/"//g' | awk -F',' '{print $5,$6,$7,$8}' | sort
```

### Export High Vulnerabilities

```bash
cat myproject.csv | grep '"High"' | sed 's/"//g' | awk -F',' '{print $5,$6,$7,$8}' | sort
```

### Export Medium Vulnerabilities

```bash
cat myproject.csv | grep '"Medium"' | sed 's/"//g' | awk -F',' '{print $5,$6,$7,$8}' | sort
```

### Export Low Vulnerabilities

```bash
cat myproject.csv | grep '"Low"' | sed 's/"//g' | awk -F',' '{print $5,$6,$7,$8}' | sort
```

