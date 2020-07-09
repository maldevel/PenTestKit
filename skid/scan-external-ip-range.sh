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
  echo "For better results, please run this script as root." 1>&2
  exit 1
fi


if [ $# -eq 1 ]; then

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

mkdir -p raw-data/live-hosts
mkdir -p raw-data/ports/tcp
mkdir -p raw-data/ports/udp
mkdir -p raw-data/services/tcp
mkdir -p raw-data/services/udp
mkdir -p scripts
mkdir -p data

cd raw-data/live-hosts

echo "Running an ICMP ECHO live hosts scan..."
echo
$dir/../live-hosts/discover-live-hosts-icmp-echo.sh $1
echo

echo "Running a Protocol Ping live hosts scan..."
echo
$dir/../live-hosts/discover-live-hosts-protocol-ping.sh $1
echo

echo "Running a Timestamp live hosts scan..."
echo
$dir/../live-hosts/discover-live-hosts-timestamp.sh $1
echo

echo "Running an IP Geolocation live hosts scan..."
echo
$dir/../live-hosts/discover-live-hosts-ip-geolocation.sh $1
echo

echo "Running a TOP 100 TCP ports live hosts scan..."
echo
$dir/../live-hosts/discover-live-hosts-top100.sh $1
echo

echo "Discovered Unique live hosts..."
echo
$dir/../grep/grep-unique-live-hosts.sh ./ | tee ../../data/unique-live-hosts.txt
echo

cd ../../

echo "Generating Nmap scans scripts..."
echo
$dir/../generate-scripts-lists/generate-tcp-full-scan-from-live-hosts-fast-noping-nodns.sh raw-data/live-hosts > scripts/tcp-full-scan.sh
chmod a+x scripts/tcp-full-scan.sh
$dir/../generate-scripts-lists/generate-tcp-top1000-scan-from-live-hosts-fast-noping-nodns.sh raw-data/live-hosts > scripts/tcp-top1000-scan.sh
chmod a+x scripts/tcp-top1000-scan.sh
$dir/../generate-scripts-lists/generate-udp-full-scan-from-live-hosts-fast-noping-nodns.sh raw-data/live-hosts > scripts/udp-full-scan.sh
chmod a+x scripts/udp-full-scan.sh
$dir/../generate-scripts-lists/generate-udp-top1000-scan-from-live-hosts-fast-noping-nodns.sh raw-data/live-hosts > scripts/udp-top1000-scan.sh
chmod a+x scripts/udp-top1000-scan.sh
echo

else
  echo "Please provide the target ip range."
fi
