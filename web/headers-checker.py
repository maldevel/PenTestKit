#!/usr/bin/python
# encoding: UTF-8

"""
    This file is part of PenTestKit
    Copyright (C) 2017-1018 @maldevel
    https://github.com/maldevel/PenTestKit

    PenTestKit - Useful tools for Penetration Testing.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    For more see the file 'LICENSE' for copying permission.

"""

__author__ = "maldevel"
__copyright__ = "Copyright (c) 2017-2018 @maldevel"
__credits__ = ["maldevel", "nma-io"]
__license__ = "GPLv3"
__version__ = "0.8"
__maintainer__ = "maldevel"

################################

import argparse
import sys
import os
import requests

from urlparse import urlparse
from termcolor import colored
from argparse import RawTextHelpFormatter

################################

from requests.packages.urllib3.exceptions import InsecureRequestWarning #remove insecure https warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #remove insecure https warning

################################

def print_request(req):
	output = '\n'
	output += '{} {} HTTP/1.1\n'.format(req.method, req.url)
	host = urlparse(req.url).hostname
	output += 'Host: {}\n'.format(host)
	output += '\n'.join(['%s: %s' % (key, value) for (key, value) in req.headers.items()])
	output += '\n'
	return output

################################

def print_response(resp, req):
	output = '\n'
	output += '\n'.join(['%s: %s' % (key, value) for (key, value) in resp.headers.items()])
	output += '\n\n[...]\n'
	return output

################################

def _analyzeHost(host, proxies):
	try:
		data = requests.get(host, verify=False, proxies=proxies, timeout=5, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'})
		req = print_request(data.request)
	except requests.exceptions.ConnectionError as e:
		print '[-] {}: Connection Error ({})'.format(host, e)
		return None, None, None
	except Exception as e:
		print '[-] {}: No Data ({})'.format(host, e)
		return None, None, None

	if not data:
		print '[-] {}: No Data'.format(host)
		return None, None, None

	if data.status_code not in range(200, 209):
		print '[-] {}: Status code {}'.format(host, data.status_code)
		return None, None, None

	print '[+] {}: {} {}'.format(host, data.status_code, requests.status_codes._codes[data.status_code][0].upper())

	resp = print_response(data, data.request)

	headers = data.headers

	return headers, req, resp

################################

def _checkHeaders(headers, https, text=False):
	results = []

	secureHeaders = {
	'X-Frame-Options':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#X-Frame-Options',
	'X-XSS-Protection':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#X-XSS-Protection',
	'X-Content-Type-Options':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#X-Content-Type-Options',
	'Content-Security-Policy':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#Content-Security-Policy',
	'X-Permitted-Cross-Domain-Policies':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#X-Permitted-Cross-Domain-Policies',
	'Referrer-Policy':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#rp',
	'Cache-control':'https://www.owasp.org/index.php/Testing_for_Browser_cache_weakness_(OTG-AUTHN-006)',
	'Pragma':'https://www.owasp.org/index.php/Testing_for_Browser_cache_weakness_(OTG-AUTHN-006)'
	}

	if https:
		secureHeaders.update({
		  'Strict-Transport-Security':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#HTTP_Strict_Transport_Security_.28HSTS.29',
		  'Public-Key-Pins':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#Public_Key_Pinning_Extension_for_HTTP_.28HPKP.29'
		})

	if text:
		for h in list(secureHeaders):
			if h not in headers:
				results.append('{}'.format(h))
	else:
		for h in list(secureHeaders):
			if h not in headers:
				results.append('{}: {}'.format(h, secureHeaders[h]))
	return results

################################

def _checkInfoLeak(headers):
	results = []

	InfoLeakHeaders = {
	'Server',
	'X-Forwarded-For',
	'X-AspNetMvc-Version',
	'X-NvRenderingEngine',
	'X-AspNet-Version',
	'X-Powered-By',
	'Via'
	}

	for h in list(InfoLeakHeaders):
		if h in headers:
			results.append('{}: {}'.format(h, headers[h]))

	return results

################################

def checkHosts(hosts, output, text, proxies, req, resp):
	http_headers_vulns = ''

	for host in hosts:
		if '://' not in host:
			print '[-] {}: Invalid host'.format(host)
			continue

		https = False
		if 'https' in host:
			https = True

		print '[+] {}: Checking headers'.format(host)

		results, reqtext, resptext = _analyzeHost(host, proxies)

		if req and reqtext:
			print '[+] {}: Request'.format(host)
			print reqtext

		if not results:
			print '[-] {}: An error occured during host analysis\n'.format(host)
			continue

		http_headers_vulns = _checkHeaders(results, https, text)
		if not http_headers_vulns:
			print '[-] {}: An error occured during secure headers analysis\n'.format(host)
			continue

		http_infoleak_vulns = _checkInfoLeak(results)
		if not http_infoleak_vulns:
			print '[-] {}: An error occured during headers information leakage analysis\n'.format(host)
			continue

		if text:
			data = '\n{}\n'.format('\n'.join(http_headers_vulns))
			data2 = '\n{}\n'.format('\n'.join(http_infoleak_vulns))
		else:
			data = '\t* {}'.format('\n\t* '.join(http_headers_vulns))
			data2 = '\t* {}'.format('\n\t* '.join(http_infoleak_vulns))

		if resp and resptext:
			print '[+] {}: Response'.format(host)
			print resptext

		print '[+] {}: Missing OWASP Secure Headers:'.format(host)
		print data

		print '[+] {}: Headers Leaking Information:'.format(host)
		print data2

		print '[+] {}: Finish'.format(host)
		print ''

		if output:
			with open('{}\{}.md'.format(output, host.replace('http://', '')), 'w') as f:
				f.write('## Target {}\n\n'.format(host))
				f.write('### Missing OWASP secure headers\n')
				f.write(data.replace('\n', '\n* ')[:-2])
				f.write('\n')
				f.write('### Headers leaking information\n')
				f.write(data2.replace('\n', '\n* ')[:-2])
				if reqtext:
					f.write('\n### HTTP Request\n\n')
					f.write('```')
					f.write('{}'.format(reqtext))
					f.write('```\n')
				if resptext:
					f.write('\n### HTTP Response\n\n')
					f.write('```')
					f.write('{}'.format(resptext))
					f.write('```\n')

################################

message = """
 _____                            _   _                _
/  ___|                          | | | |              | |
\ `--.  ___  ___ _   _ _ __ ___  | |_| | ___  __ _  __| | ___ _ __ ___
 `--. \/ _ \/ __| | | | '__/ _ \ |  _  |/ _ \/ _` |/ _` |/ _ \ '__/ __|
/\__/ /  __/ (__| |_| | | |  __/ | | | |  __/ (_| | (_| |  __/ |  \__ \\
\____/ \___|\___|\__,_|_|  \___| \_| |_/\___|\__,_|\__,_|\___|_|  |__ /

                     Headers Checker | @maldevel
                             Version: {}
""".format(__version__)


def MainFunc():
	parser = argparse.ArgumentParser(description=message, formatter_class=RawTextHelpFormatter)

	parser.add_argument("-H", "--host",
	                    action="store",
	                    metavar='hostname',
	                    dest='host',
	                    type=str,
	                    default=None,
	                    help='The host to check, e.g. http://example.com, https://example.com, http://192.168.1.1')

	parser.add_argument('-l', '--list',
	                    action='store',
	                    metavar='hostsfile',
	                    dest='hostsfile',
	                    type=str,
	                    default=None,
	                    help='Hosts list file path. Place each target host in new line.')

	parser.add_argument('-o', '--output',
	                    action='store',
	                    metavar='directory',
	                    dest='output',
	                    type=str,
	                    default=None,
	                    help='Output directory path')

	parser.add_argument('-x', '--proxy',
	                    action="store",
	                    metavar='PROXY',
	                    dest='proxy',
	                    type=str,
	                    default=None,
	                    required=False,
	                    help='Use proxy (eg. http://127.0.0.1:8080).')

	parser.add_argument('-t', '--text',
	                    action="store_true",
	                    help='Print plain text results.')

	parser.add_argument('-r', '--request',
	                    action="store_true",
	                    help='Print request raw text.')

	parser.add_argument('-e', '--response',
	                    action="store_true",
	                    help='Print response raw text.')

	if len(sys.argv) is 1:
		parser.print_help()
		sys.exit(1)

	args = parser.parse_args()

	print message

	host = args.host
	flist = args.hostsfile

	if host and flist:
		print '[-] {}: Please specify one host only (-H) or a file list of hosts (-l).'.format(host)
		sys.exit(1)

	proxies = {
	  'http': args.proxy,
	  'https': args.proxy,
	}

	if host:
		checkHosts([args.host], args.output, args.text, proxies, args.request, args.response)
	elif flist:
		hosts = []
		with open(flist, 'r') as f:
			hosts = f.read().splitlines()
		checkHosts(hosts, args.output, args.text, proxies, args.request, args.response)


if __name__ == '__main__':
	try:
		MainFunc()
	except KeyboardInterrupt:
		print "Interrupted by user.."
	except:
		sys.exit()
