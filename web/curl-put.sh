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


# e.g. $1 == Accept header
# e.g. $2 == Content Type header
# e.g. $3 == Auth Cookie header
# e.g. $4 == put data
# e.g. $5 == proxy (http://127.0.0.1:8080)
# e.g. $6 == target url

if [ $# -eq 6 ]; then
	curl -X PUT --header "$1" --header "$2" --header 'Accept-Language: en' --header "$3" -d "$4" -x "$5" --insecure --include "$6"
else
    echo "Please provide Accept header, content-type, authorization cookie, put data, proxy server and target url."
fi
