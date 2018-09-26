#!/usr/bin/python
# encoding: UTF-8

"""
    This file is part of PenTestKit
    Copyright (C) 2017-2018 @maldevel
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
__credits__ = ["maldevel"]
__license__ = "GPLv3"
__version__ = "0.2"
__maintainer__ = "maldevel"

################################

import argparse
import sys
import os
import requests
import socket
import ssl

from bs4 import BeautifulSoup, Comment
from termcolor import colored
from argparse import RawTextHelpFormatter
from urlparse import urlparse

################################

from requests.packages.urllib3.exceptions import InsecureRequestWarning #remove insecure https warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #remove insecure https warning

################################

def yellow(text):
    return colored(text, 'yellow', attrs=['bold'])

def green(text):
    return colored(text, 'green', attrs=['bold'])

def red(text):
    return colored(text, 'red', attrs=['bold'])

def cyan(text):
    return colored(text, 'cyan', attrs=['bold'])

def magenta(text):
    return colored(text, 'magenta', attrs=['bold'])

def blue(text):
    return colored(text, 'blue', attrs=['bold'])

################################

message = """
 __          __  _     _____                      
 \ \        / / | |   |  __ \                     
  \ \  /\  / /__| |__ | |__) |___  ___ ___  _ __  
   \ \/  \/ / _ \ '_ \|  _  // _ \/ __/ _ \| '_ \ 
    \  /\  /  __/ |_) | | \ \  __/ (_| (_) | | | |
     \/  \/ \___|_.__/|_|  \_\___|\___\___/|_| |_|

       Web Application Reconnaissance | @maldevel                
                                     {}: {}
""".format(blue('Version'), green(__version__)) 

###########################

def parseArgs():
    parser = argparse.ArgumentParser(description=message, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-u", "--url", action="store", metavar='URL', dest='url', type=str,
                        default=None, required=True,
                        help='The url to scan, e.g. http://example.com, https://example.com, http://192.168.1.1')
    parser.add_argument('-o', '--output', action='store', metavar='LOGFILE', dest='logs', type=str, default=None,
                        help='Log file path')
    args = parser.parse_args()

    return args

###########################

def find_headers(url, logfile):

    print magenta('[+] Headers')
    if logfile:
        logfile.write('### Headers\n\n')

    try:
        r = requests.head(url, verify=False)
    except:
        print red("[-] An error has occured: {}.\n".format(sys.exc_info()[0]))
        return False

    for key, value in r.headers.items() :
        print '{} {}: {}'.format(green('>'), key, value)
        if logfile:
            logfile.write('* {}: {}\n'.format(key, value))


def find_title(html, logfile):
    soup = BeautifulSoup(html, 'lxml') #html5lib

    print magenta('[+] Title')
    if logfile:
        logfile.write('### Title\n\n')

    title = soup.find('title')
    print '{} {}'.format(green('>'), title)
    if logfile:
        logfile.write('```\n{}\n```\n\n'.format(title))


def find_meta(html, logfile):
    soup = BeautifulSoup(html, 'lxml') #html5lib

    print magenta('[+] Meta tags')
    if logfile:
        logfile.write('### Meta tags\n\n')

    for tag in soup.find_all('meta'):
        print '{} {}'.format(green('>'), tag)
        if logfile:
            logfile.write('```html\n{}\n```\n\n'.format(tag))


def find_comments(html, logfile):
    soup = BeautifulSoup(html, 'lxml') #html5lib

    print magenta('[+] HTML Comments')
    if logfile:
        logfile.write('### HTML Comments\n\n')

    for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
        print '{} {}'.format(green('>'), comment)
        if logfile:
            logfile.write('```html\n{}\n```\n\n'.format(comment))

##########################

def socket_request(hostname, request, port=80, https=False):
    CRLF = "\r\n"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    if https:
        s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)

    try:
        s.connect((hostname, port))
    except:
        print red("[-] An error has occured: {}.\n".format(sys.exc_info()[0]))
        return False

    s.send(CRLF.join(request))

    response = b''

    buffer = s.recv(4096)
    while buffer:
        response += buffer
        buffer = s.recv(4096)

    header, _, body = response.partition(CRLF + CRLF)
    s.close()

    return header


def malformed_request(url, logfile, port=80, https = False):
    hostname = urlparse(url).hostname

    request1 = [
        "GET / HTTP/3.1",
        "Host: {}".format(hostname),
        "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Accept: text/html",
        "Accept-Language: en-US,en;q=0.5",
        "Content-Length: 0",
        "Connection: Close",
        "",
        ""
    ]

    request2 = [
        "GET / JUNK/1.1",
        "Host: {}".format(hostname),
        "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Accept: text/html",
        "Accept-Language: en-US,en;q=0.5",
        "Content-Length: 0",
        "Connection: Close",
        "",
        ""
    ]

    request3 = [
        "GET /%00",
        "",
        ""
    ]

    if logfile:
        logfile.write('### Malformed Requests\n\n')

    print magenta('[+] Malformed Request - Invalid HTTP Version number')
    if logfile:
        logfile.write('#### Invalid HTTP Version number\n\n**Response**\n\n')

    resp1 = socket_request(hostname, request1)
    if resp1:
        print '{} {}'.format(green('>'), resp1)
        if logfile:
            logfile.write('```html\n{}\n```\n\n'.format(resp1))

        print ''

    print magenta('[+] Malformed Request - Invalid Protocol')
    if logfile:
        logfile.write('#### Invalid Protocol\n\n**Response**\n\n')

    resp2 = socket_request(hostname, request2)
    if resp2:
        print '{} {}'.format(green('>'), resp2)
        if logfile:
            logfile.write('```html\n{}\n```\n\n'.format(resp2))

        print ''

    print magenta('[+] Malformed Request - Null')
    if logfile:
        logfile.write('#### Null\n\n**Response**\n\n')

    resp3 = socket_request(hostname, request3)
    if resp3:
        print '{} {}'.format(green('>'), resp3)
        if logfile:
            logfile.write('```html\n{}\n```\n\n'.format(resp3))

##########################

def check_secureheaders(url, logfile, https):
    results = []

    secureHeaders = {
        'X-Frame-Options':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#X-Frame-Options',
        'X-XSS-Protection':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#X-XSS-Protection',
        'X-Content-Type-Options':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#X-Content-Type-Options',
        'Content-Security-Policy':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#Content-Security-Policy',
        'X-Permitted-Cross-Domain-Policies':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#X-Permitted-Cross-Domain-Policies'
        }

    if https:
        secureHeaders.update({
          'Strict-Transport-Security':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#HTTP_Strict_Transport_Security_.28HSTS.29',
          'Public-Key-Pins':'https://www.owasp.org/index.php/OWASP_Secure_Headers_Project#Public_Key_Pinning_Extension_for_HTTP_.28HPKP.29'
        })


    headers = requests.get(url, verify=False).headers

    print magenta('[+] Missing Secure Headers')
    if logfile:
        logfile.write('### Missing Secure Headers\n\n')

    for h in list(secureHeaders):
        if h not in headers:
            print '{} {}: {}'.format(green('>'), h, secureHeaders[h])
            if logfile:
                logfile.write('* [{}]({})\n'.format(h, secureHeaders[h]))

    if logfile:
        logfile.write('\n')

def find_robotstxt(url, logfile):
    txt = requests.get("{}/robots.txt".format(url), verify=False, stream=True).text

    print magenta('[+] Robots.txt')
    if logfile:
        logfile.write('### Robots.txt\n\n')

    print '{} {}'.format(green('>'), txt)
    if logfile:
        logfile.write('```\n{}\n```\n\n'.format(txt))

def check_cacheheaders(url, logfile):
    results = []

    cacheHeaders = {
        'Cache-control':'no-store',
        'Pragma':'no-cache'
        }

    headers = requests.get(url, verify=False).headers

    print magenta('[+] Missing Caching directives')
    if logfile:
        logfile.write('### Missing caching directives (Cacheable HTTPS response)\n\n')

    for h in list(cacheHeaders):
        if h not in headers or headers[h] != cacheHeaders[h]:
            print '{} {}: {}'.format(green('>'), h, cacheHeaders[h])
            if logfile:
                logfile.write('* [{}]({})\n'.format(h, cacheHeaders[h]))

    if logfile:
        logfile.write('\n')


if __name__ == '__main__':

    args = parseArgs()
    print message

    url = args.url
    logs = False
    https = False
    port = 80

    if args.logs:
        filepath = args.logs
        if not filepath.endswith('.md'):
            filepath = filepath + '.md'
        logs = open(filepath, 'w')

    if 'https' in url:
        https = True

    if url.count(":") == 2:
        port = url.rsplit(':', 1)[1]

    if '://' not in url:
        print red('[-] {}: Invalid url'.format(url))
        sys.exit(1)

    if logs:
        logs.write('## Web Application Reconnaissance\n')
        logs.write('\n***\n')
        logs.write('\n')

    if find_headers(url, logs):
        if logs:
            logs.write('\n***\n\n')

    print ''

    html = requests.get(url, verify=False).content

    find_title(html, logs)
    print ''
    if logs:
        logs.write('***\n\n')

    find_meta(html, logs)
    print ''
    if logs:
        logs.write('***\n\n')

    find_comments(html, logs)
    print ''
    if logs:
        logs.write('***\n\n')

    malformed_request(url, logs, port, https)
    print ''
    if logs:
        logs.write('***\n\n')

    check_secureheaders(url, logs, https)
    print ''
    if logs:
        logs.write('***\n\n')

    find_robotstxt(url, logs)
    print ''
    if logs:
        logs.write('***\n\n')

    check_cacheheaders(url, logs)
    print ''
    if logs:
        logs.write('***\n\n')
