#!/bin/bash

#    This file is part of PenTestKit
#    Copyright (C) 2017-2018 @maldevel
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


if [ $# -eq 2 ]; then

oldvuln=""
echo "### $2"

cat $1 | grep "\"$2\"" | sed 's/"//g' | awk -F',' 'BEGIN { OFS = ";" }{ print $8, $5, $6, $7 }' | sort | while read -r line ; do

  vuln=$(echo $line | awk -F';' '{print $1}')
  ip=$(echo $line | awk -F';' '{print $2}')
  proto=$(echo $line | awk -F';' '{print $3}')
  port=$(echo $line | awk -F';' '{print $4}')

  if [ "$vuln" != "$oldvuln" ]; then
    if [ "$oldvuln" != "" ]; then
      echo
    fi
    echo
    echo "#### $vuln"
    echo
    echo -n "* $ip ($proto/$port), "
  else
    echo -n "$ip ($proto/$port), "
  fi
  oldvuln=$vuln

done
echo
echo
echo "---"
echo
else
    echo "Please provide a Nessus CSV file and the Risk rate(Critical, High, Medium, Low)."
fi
