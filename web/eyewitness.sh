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



if [ $# -eq 3 ]; then
	python3 /opt/EyeWitness/Python/EyeWitness.py --web -f "$1" -d "$2" --user-agent "$3" --prepend-https --no-prompt
else
    echo "Please provide a Line seperated file containing URLs to capture, a Directory name for report output and a User-Agent string."
fi
