import scanner

target_url = 'http://10.0.2.30/'
ignore_links = ["http://10.0.2.30/dvwa/logout.php"]

vuln_scanner = scanner.Scanner(target_url, ignore_links)

# values for login page if required else comment these
login_post_values = {"username":"admin", "password":"password", "Login":"submit"}
vuln_scanner.session.post('http://10.0.2.30/dvwa/login.php', data=login_post_values)

# test cases
# forms = vuln_scanner.get_forms('http://10.0.2.30/dvwa/vulnerabilities/xss_r/')
# is_vulnerable = vuln_scanner.is_xss_vulnerable_in_form(forms[0], 'http://10.0.2.30/dvwa/vulnerabilities/xss_r/')

# print(is_vulnerable)

# is_link_vuln = vuln_scanner.is_xss_vulnerable_in_link('http://10.0.2.30/dvwa/vulnerabilities/xss_r/?name=test')
# print(is_link_vuln)

vuln_scanner.run()