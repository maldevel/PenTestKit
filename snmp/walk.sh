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


if [ $# -eq 1 ]; then
	snmpwalk -c public -v 1 $1 2>&1 | tee "snmpwalk.txt"

    snmpwalk -c public -v 1 $1 1.3.6.1.2.1.25.1.6.0 2>&1 | tee "snmpwalk_system_processes.txt"

    snmpwalk -c public -v 1 $1 1.3.6.1.2.1.25.4.2.1.2 2>&1 | tee "snmpwalk_running_processes.txt"

    snmpwalk -c public -v 1 $1 1.3.6.1.2.1.25.4.2.1.4 2>&1 | tee "snmpwalk_process_paths.txt"

    snmpwalk -c public -v 1 $1 1.3.6.1.2.1.25.2.3.1.4 2>&1 | tee "snmpwalk_storage_units.txt"

    snmpwalk -c public -v 1 $1 1.3.6.1.2.1.25.6.3.1.2 2>&1 | tee "snmpwalk_software_names.txt"

    snmpwalk -c public -v 1 $1 1.3.6.1.4.1.77.1.2.25 2>&1 | tee "snmpwalk_user_accounts.txt"

    snmpwalk -c public -v 1 $1 1.3.6.1.2.1.6.13.1.3 2>&1 | tee "snmpwalk_tcp_ports.txt"

else
    echo "Please provide a target host."
fi
