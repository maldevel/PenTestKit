#!/usr/bin/python
# encoding: UTF-8

"""
    This file is part of PenTestKit
    Copyright (C) 2017-1019 @maldevel
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
__copyright__ = "Copyright (c) 2017-2019 @maldevel"
__credits__ = ["maldevel"]
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "maldevel"

#######################################################################################################

import sys
import argparse
import os
import json

from argparse import RawTextHelpFormatter

#######################################################################################################

message = """
Parse Docker-Bench-Security Script JSON files | @maldevel
Version: {}
""".format(__version__)

def MainFunc():
    parser = argparse.ArgumentParser(description=message, formatter_class=RawTextHelpFormatter)

    parser.add_argument('-j', '--json',
                        action='store',
                        metavar='jsonfile',
                        dest='jsonfile',
                        type=str,
                        default=None,
                        help='Results json file path.')

    parser.add_argument('-t', '--type',
                        action='store',
                        metavar='type',
                        dest='type',
                        type=str,
                        default='all',
                        help='Result type(info, pass, warn, note, all).')

    parser.add_argument('-f', '--filename',
	                    action='store',
	                    metavar='filename',
	                    dest='filename',
	                    type=str,
	                    default=None,
	                    help='Output filename')

    parser.add_argument('-o', '--output',
	                    action='store',
	                    metavar='directory',
	                    dest='output',
	                    type=str,
	                    default=None,
	                    help='Output directory path')

    if len(sys.argv) is 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    print (message)

    jsonfile = args.jsonfile
    if not os.path.isfile(jsonfile):
        print ('[-] Please provide an existing json file.')
        sys.exit(1)

    with open(jsonfile, "r") as f:
        data = json.load(f)

    filter = args.type.lower()

    filename = args.filename

    if filename:
        txtfilename = filename + ".txt"
        mdfilename = filename + ".md"
        htmlfilename = filename + ".html"
    else:
        txtfilename = os.path.basename(jsonfile) + ".txt"
        mdfilename = os.path.basename(jsonfile) + ".md"
        htmlfilename = os.path.basename(jsonfile) + ".html"

    output = args.output

    if output:
        txtfile = os.path.join(output, '') + txtfilename
        mdfile = os.path.join(output, '') + mdfilename
        htmlfile = os.path.join(output, '') + htmlfilename
    else:
        txtfile = os.path.join(os.path.dirname(jsonfile), '') + txtfilename
        mdfile = os.path.join(os.path.dirname(jsonfile), '') + mdfilename
        htmlfile = os.path.join(os.path.dirname(jsonfile), '') + htmlfilename

    with open(txtfile, "w") as txt, open(mdfile, "w") as md, open(htmlfile, "w") as html: 
        print('Docker Bench Security {} Results\n'.format(data['dockerbenchsecurity']))
        txt.write('Docker Bench Security {} Results\n\n'.format(data['dockerbenchsecurity']))
        txt.write('Checks: {}\n'.format(data['checks']))
        txt.write('Score: {}\n\n'.format(data['score']))

        md.write('## Docker Bench Security {} Results\n\n'.format(data['dockerbenchsecurity']))
        md.write('* Checks: {}\n'.format(data['checks']))
        md.write('* Score: {}\n'.format(data['score']))
        md.write('\n')

        html.write('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Docker Bench Security {} Results</title></head><body>'.format(data['dockerbenchsecurity']))
        html.write('<h2>Docker Bench Security {} Results</h2>'.format(data['dockerbenchsecurity']))
        html.write('<ul>')
        html.write('<li><b>Checks</b>: {}</li>'.format(data['checks']))
        html.write('<li><b>Score</b>: {}</li>'.format(data['score']))
        html.write('</ul>')

        for test in data['tests']:
            print('{}\n'.format(test['desc']))
            txt.write('{}\n\n'.format(test['desc']))
            md.write('### {}\n\n'.format(test['desc']))
            html.write('<h3>{}</h3>'.format(test['desc']))

            html.write('<ul>')
            for result in test['results']:

                if result['result'] == 'WARN' and (filter == 'warn' or filter == 'all'):
                    print('[{}] {} {}'.format(result['result'], result['id'], result['desc']))
                    txt.write('[{}] {} {}\n'.format(result['result'], result['id'], result['desc']))
                    md.write('* [{}] {} {}\n'.format(result['result'], result['id'], result['desc']))
                    html.write('<li> [<font color="red"><b>{}</b></font>] '.format(result['result']))
                    html.write('{} {}</li>'.format(result['id'], result['desc']))

                elif result['result'] == 'INFO' and (filter == 'info' or filter == 'all'):
                    print('[{}] {} {}'.format(result['result'], result['id'], result['desc']))
                    txt.write('[{}] {} {}\n'.format(result['result'], result['id'], result['desc']))
                    md.write('* [{}] {} {}\n'.format(result['result'], result['id'], result['desc']))
                    html.write('<li> [<font color="blue"><b>{}</b></font>] '.format(result['result']))
                    html.write('{} {}</li>'.format(result['id'], result['desc']))

                elif result['result'] == 'PASS' and (filter == 'pass' or filter == 'all'):
                    print('[{}] {} {}'.format(result['result'], result['id'], result['desc']))
                    txt.write('[{}] {} {}\n'.format(result['result'], result['id'], result['desc']))
                    md.write('* [{}] {} {}\n'.format(result['result'], result['id'], result['desc']))
                    html.write('<li> [<font color="green"><b>{}</b></font>] '.format(result['result']))
                    html.write('{} {}</li>'.format(result['id'], result['desc']))

                elif result['result'] == 'NOTE' and (filter == 'note' or filter == 'all'):
                    print('[{}] {} {}'.format(result['result'], result['id'], result['desc']))
                    txt.write('[{}] {} {}\n'.format(result['result'], result['id'], result['desc']))
                    md.write('* [{}] {} {}\n'.format(result['result'], result['id'], result['desc']))
                    html.write('<li> [<font color="orange"><b>{}</b></font>] '.format(result['result']))
                    html.write('{} {}</li>'.format(result['id'], result['desc']))

            html.write('</ul>')

            print()
            txt.write('\n')
            md.write('\n---\n\n')
            html.write('<br><hr>')

        html.write('</body></html>')

#######################################################################################################

if __name__ == '__main__':
    try:
        MainFunc()
    except KeyboardInterrupt:
        print ("Interrupted by user..")
    except:
        sys.exit()

#######################################################################################################
