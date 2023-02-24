# Vuln Scanner

## sqli.py

- Search for php websites using search engine

    ```text
    inurl:.php?id
    ```

- Use sqli.py to test the WebApp

    ```bash
    python3 sqli.py -u [url]
    ```

## Test Scans

### test case 1: Testing on DVWA metasploitable

- target_url = http://10.0.2.30/dvwa
- login_link = http://10.0.2.30/dvwa/login.php
- ignore_links = http://10.0.2.30/dvwa/logout.php
- ld = ['admin','password']

Usage:

```bash
$ python3 vuln_scanner.py -t http://10.0.2.30/dvwa/ -ig http://10.0.2.30/dvwa/logout.php -l http://10.0.2.30/dvwa/login.php -ld admin,password
```

### Test Case 2: Testing on mutillidae 

Usage:

```bash
$ python3 vuln_scanner.py -t http://10.0.2.30/mutillidae/   
```
