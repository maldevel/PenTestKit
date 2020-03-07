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
  LOGNAME="live_hosts_tcp_ack_$1"
  LOGNAME=$(echo "$LOGNAME" | sed -r 's/[/]+/_/g' | sed -r 's/[.]+/_/g')
  nmap -vv -n -sn -PA21,22,23,25,53,80,88,110,135,139,143,443,445,465,587,993,995,1433,3306,3389,8080,8443 -oA $LOGNAME $1

  LOGNAME="live_hosts_icmp_echo_$1"
  LOGNAME=$(echo "$LOGNAME" | sed -r 's/[/]+/_/g' | sed -r 's/[.]+/_/g')
  nmap -vv -n -sn -PE -oA $LOGNAME $1

  LOGNAME="live_hosts_tcp_protocol_ping_$1"
  LOGNAME=$(echo "$LOGNAME" | sed -r 's/[/]+/_/g' | sed -r 's/[.]+/_/g')
  nmap -vv -n -sn -PO -oA $LOGNAME $1

  LOGNAME="live_hosts_sctp_$1"
  LOGNAME=$(echo "$LOGNAME" | sed -r 's/[/]+/_/g' | sed -r 's/[.]+/_/g')
  nmap -vv -n -sn -PY2905 -oA $LOGNAME $1

  LOGNAME="live_hosts_tcp_syn_$1"
  LOGNAME=$(echo "$LOGNAME" | sed -r 's/[/]+/_/g' | sed -r 's/[.]+/_/g')
  nmap -vv -n -sn -PS21,22,23,25,53,80,88,110,135,139,143,443,445,465,587,993,995,1433,3306,3389,8080,8443 -oA $LOGNAME $1

  LOGNAME="live_hosts_timestamp_$1"
  LOGNAME=$(echo "$LOGNAME" | sed -r 's/[/]+/_/g' | sed -r 's/[.]+/_/g')
  nmap -vv -n -sn -PP -oA $LOGNAME $1

  LOGNAME="live_hosts_tcp_top100_$1"
  LOGNAME=$(echo "$LOGNAME" | sed -r 's/[/]+/_/g' | sed -r 's/[.]+/_/g')
  nmap -sS -n -Pn --top-ports 100 --reason --open -T4 -oA $LOGNAME $1

  LOGNAME="live_hosts_udp_$1"
  LOGNAME=$(echo "$LOGNAME" | sed -r 's/[/]+/_/g' | sed -r 's/[.]+/_/g')
  nmap -vv -n -sn -PU53,67,123,135,137,138,161,445,631,1434 -oA $LOGNAME $1

  
else
    echo "Please provide the target IP range."
fi
