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

  echo "#!/bin/bash"
  echo

  echo "if [[ \$EUID -ne 0 ]]; then"
  echo "'Please run this script as root.' 1>&2"
  echo "exit 1"
  echo "fi"
  echo

  cat $1/*.gnmap | grep 'Status: Up' | cut -d ' ' -f2 | sort -V | uniq| while read -r host ; do

  	echo "nmap -sS -n -Pn -vv --top-ports 1000 --reason --open -T4 -oA tcp_ports_full_$host $host &"

  done
  echo "wait"
  echo

else
  echo "Please provide a directory path."
fi
