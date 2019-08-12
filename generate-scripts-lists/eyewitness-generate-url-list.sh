#!/bin/bash

#    This file is part of PenTestKit
#    Copyright (C) 2017-2019 @maldevel
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


if [ $# -eq 1 ]; then

  cat $1/*.gnmap | grep "/open/tcp//http\|/open/tcp//ssl" | while read -r line ; do
    host=`echo "$line"|cut -d$'\t' -f1|cut -d' ' -f2`
    ports=`echo "$line"|cut -d$'\t' -f2|sed 's/Ports: //'`

    IFS=","
    space=","
    hostports=""
    webports=""

    for port in $ports; do
      openports=$(expr match "$port" '\(.*\(open\|open|filtered\)/\(tcp\|udp\).*\)')
      if [ -n "$openports" ]; then
    ports=`echo "$openports"|tr "," "\n"`
    if [ -n "$ports" ]; then
      for port in $ports; do
        if echo "$port" | grep -q "/open/tcp//http\|/open/tcp//ssl"; then 
          webports=$webports$(echo $port|sed 's|/| |g'|sed -n -e 's/open.*//p'|sed 's/ *//g')$space
        fi
      done
    fi
      fi
    done

      if [ -n "$webports" ]; then
    oldIFS=$IFS
    IFS=","
    for port in $webports; do
      echo "$host:$port"
    done
    IFS=$oldIFS
      fi
  done

else
  echo "Please provide a directory path."
fi
