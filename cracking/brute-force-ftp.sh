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
msfconsole -n -q -r - << EOF
use auxiliary/scanner/ftp/ftp_login
set BLANK_PASSWORDS true
set BRUTEFORCE_SPEED 5
set PASS_FILE /usr/share/metasploit-framework/data/wordlists/unix_passwords.txt
set RHOSTS $1
set STOP_ON_SUCCESS true
set THREADS 20
set USER_AS_PASS true
set USER_FILE /usr/share/metasploit-framework/data/wordlists/unix_users.txt
run
exit
EOF
else
    echo "Please provide the target FTP server."
fi
