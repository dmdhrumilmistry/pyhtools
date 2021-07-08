#!usr/bin/env python3
import scanner

target_url = 'http://10.0.2.30/dvwa/vulnerabilities/xss_r/'
ignore_links = ["http://10.0.2.30/dvwa/logout.php"]

vuln_scanner = scanner.Scanner(target_url, ignore_links)

login_post_values = {"username":"admin", "password":"password", "Login":"submit"}
vuln_scanner.session.post('http://10.0.2.30/dvwa/login.php', data=login_post_values)

vuln_scanner.run()