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

if [ $# -eq 1 ]; then

  egrep -v "^#|Status: Up" $1/*.gnmap|cut -d' ' -f2,4-|sed 's/Ignored.*//g' |sed 's/ /'$'_''/'|sed 's/, /,/g'| awk -v FS=_ '{printf "Host: " $1 "\nOpen ports: " NF "\n"; $1=""; for(i=2; i<=NF; i++){ a=a""$i; }; split(a,s,","); for(e in s) { split(s[e],v,"/"); printf "%-10s%-20s%s\n", v[1], v[5], v[7]}; a=""; printf "\n"; }'
else
  echo "Please provide a directory path."
fi
