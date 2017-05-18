#!/usr/bin/python
# encoding: UTF-8

"""
    This file is part of PenTestKit
    Copyright (C) 2017 @maldevel
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
__copyright__ = "Copyright (c) 2017 @maldevel"
__credits__ = ["maldevel", "nma-io"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "maldevel"


import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys
import os
import argparse
from argparse import RawTextHelpFormatter
from termcolor import colored


def yellow(text):
    return colored(text, 'yellow', attrs=['bold'])

def green(text):
    return colored(text, 'green', attrs=['bold'])

def red(text):
    return colored(text, 'red', attrs=['bold'])

def cyan(text):
    return colored(text, 'cyan', attrs=['bold'])

def load_request(filename):
  post_data = ''
  headers = {}
  method = ''
  uri = ''

  with open(filename) as f: 
    index = 0
    potential_data = False

    for line in f:
      if index == 0:  
        first_line = line
        if ' ' not in first_line:
          raise Exception('[-] Invalid request file!')

        first_line = first_line.split(' ')
        method = first_line[0].lower() #GET POST etc
        uri = first_line[1]
        index = 1
        continue

      if potential_data:
        post_data = line
        break

      if ':' in line:
        words = line.split(':', 1)  
        headers[words[0].strip()] = words[1].strip()

      if line.strip() == '':  
        potential_data = True

    url = '{}://{}{}'.format('https', headers['Host'], uri)

  return url, headers, post_data, method


def load_contentTypes(filename, ack = True):
    u = [] 

    if ack:
        print '[+] Loading content types from file {}...'.format(filename)

    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
              continue
            if '/' in line:
                u.append(line.strip())
    
    return u


def main():
    parser = argparse.ArgumentParser(description='{}'.format(red('Test Content Types')), formatter_class=RawTextHelpFormatter)

    parser.add_argument("-t", "--content-types", 
                        action="store", 
                        metavar='FILE',
                        dest='contentTypesFile', 
                        type=str, 
                        default=None, 
                        required=True, 
                        help='File containing contant types.')
    
    parser.add_argument("-r", "--request", 
                        action="store", 
                        metavar='FILE',
                        dest='requestFile', 
                        type=str, 
                        default=None, 
                        required=True, 
                        help='File containing http request (burp format).')
    
    parser.add_argument("-o", "--output",
                        action="store",
                        metavar='FILE',
                        dest='outputFile',
                        type=str,
                        default=None,
                        required=True,
                        help='File to write results.')
    
    parser.add_argument('-x', '--proxy', 
                        action="store", 
                        metavar='PROXY', 
                        dest='proxy', 
                        type=str,
                        default=None, 
                        required=True, 
                        help='Use proxy (eg. http://127.0.0.1:8080).')
    
    
    if len(sys.argv) is 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()
    
    if (not os.path.isfile(args.requestFile)):
      print red('[-] Please provide an existing request file.')
      sys.exit()
    
    if (not os.path.isfile(args.contentTypesFile)): 
         print red('[-] Please provide an existing content types file.')
         sys.exit()
         

    contentTypes = load_contentTypes(args.contentTypesFile, False)
    length = len(contentTypes)
    if length ==0:
        print red('[-] Content Types file is empty\n')
        
    i=1
    
    proxies = {
      'http': args.proxy,
      'https': args.proxy,
    }

    with open(args.outputFile, 'a') as ptfile: 
      for ct in contentTypes:
        
        print '[+] {}/{}({}%)\n'.format(i, length, (i*100)/length)    #progress
        print '[+] Checking content type {}'.format(cyan(ct))

        requestName = os.path.splitext(os.path.basename(args.requestFile))[0]
        print '[+] Request: {}'.format(cyan(requestName))
                   
        url, headers, post_data, method = load_request(args.requestFile)
        headers['Content-Type']=ct

        try:
          r = getattr(requests, method)(url, proxies=proxies, verify=False,headers=headers, data=post_data)
        except:
          print red('[-] Unexpected error')
          continue

        ptfile.write('{}:{}:{} {}\n'.format(ct, requestName, r.status_code, requests.status_codes._codes[r.status_code][0].upper()))
        print yellow('[+] {} {}').format(r.status_code, requests.status_codes._codes[r.status_code][0].upper())
        print ''
      
        i += 1
 

if __name__ == '__main__':
  main()
 

