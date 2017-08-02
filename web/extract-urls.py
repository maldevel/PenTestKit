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

##################################################

__author__ = "maldevel"
__copyright__ = "Copyright (c) 2017 @maldevel"
__credits__ = ["maldevel"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "maldevel"

##################################################

from datetime import datetime
import signal
from urllib2 import urlopen
import re
import os
import sys
import argparse
from argparse import RawTextHelpFormatter
from termcolor import colored

##################################################

def yellow(text):
    return colored(text, 'yellow', attrs=['bold'])

def green(text):
    return colored(text, 'green', attrs=['bold'])

def red(text):
    return colored(text, 'red', attrs=['bold'])

def cyan(text):
    return colored(text, 'cyan', attrs=['bold'])

def signal_handler(signal, frame):
    sys.exit(0)

##################################################

def main():
    parser = argparse.ArgumentParser(description='{}'.format(cyan('Extract URLs')), formatter_class=RawTextHelpFormatter)

    parser.add_argument("-f", "--filename", action="store", metavar='FILE', dest='filename',  type=str, default=None, required=True, help='File containing urls.')
    parser.add_argument("-o", "--output", action="store", metavar='FILE', dest='outputFile', type=str, default='log.txt', required=False, help='File to write results.')

    if len(sys.argv) is 1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    print '\n[*] Extract URLs from file.'

    if (not os.path.isfile(args.filename)):
        print red('[-] Please provide an existing file.\n')
        sys.exit()

    with open(args.outputFile, 'a') as logfile:

        logfile.write('\n---\n\n')

        print '[*] Reading file {}..'.format(args.filename)
        logfile.write('{}: Reading file {}\n'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), args.filename))

        filename = open(args.filename)
        content = filename.read()

        print '[*] Extracting URLs..'
        logfile.write('{}: Extracting URLs..\n'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))

        urls = re.findall(r'(?P<url>https?://[^\s]+)', content)#(https?://\S+)
        urls = [u.replace(')', '') for u in urls]   #markdown urls contain ) at the end of url
        
        print green('[*] Found {} URLs.'.format(len(urls)))
        logfile.write('{}: Found {} URLs.\n'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), len(urls)))
        
        print '[*] Validating URLs..'
        logfile.write('{}: Validating URLs..\n'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))

        invalidUrls = 0
        validUrls = 0

        for u in urls:
            dt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
            code = urlopen(u).code
            if (code / 100 >= 4):
                print red('[-] Invalid URL ({}) {}'.format(code, u))
                logfile.write('{}: Invalid URL ({}) {}\n'.format(dt, code, u))
                invalidUrls += 1
            else:
                print green('[+] Valid URL ({}) {}'.format(code, u))
                logfile.write('{}: Valid URL ({}) {}\n'.format(dt, code, u))
                validUrls += 1

        print '\n'
        print '[*] Valid URLs: {}'.format(validUrls)
        logfile.write('Valid URLs: {}\n'.format(validUrls))
        print '[*] Invalid URLs: {}'.format(invalidUrls)
        logfile.write('Invalid URLs: {}\n'.format(invalidUrls))

    print '\n'

##################################################

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()

