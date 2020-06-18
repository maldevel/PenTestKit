#!/bin/bash

#    This file is part of PenTestKit
#    Copyright (C) 2017-2020 @maldevel
#    https://github.com/maldevel/PenTestKit
#
#    PenTestKit - Useful tools for Penetration Testing.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    For more see the file 'LICENSE' for copying permission.


if [[ $EUID -ne 0 ]]; then
  echo "Please run this script as root." 1>&2
  exit 1
fi

if [ $# -eq 1 ]; then
	nmap -sS -n -T0 -Pn -vv -p21,22,25,53,80,110,135,137,139,143,443,445,465,587,981,993,995,1194,1433,2525,3306,3389,5060,5061,7777,8006,8008,8080,8090,8333,8880,8888,8443,9000,9001 --reason --open --max-rate 0.1 --host-timeout 30m --scan-delay 1s --max-retries 1 -oA tcp_top_ports_$1 $1
else
    echo "Please provide the target IP address or an IP range."
fi
