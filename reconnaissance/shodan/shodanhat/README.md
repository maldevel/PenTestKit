# Dependencies
You need to install shodan with pip install shodan or easy_install shodan.<br />
You need to install python-nmap with pip install python-nmap.<br />
You need to set your API Key in the 'constantes.py' file.

# Options
-h, --help                 show this help message and exit<br />
-i IP, --ip=IP             info about one host<br />
-l LIST, --list=LIST       info about a list of hosts<br />
-s SQ, --sq=SQ             searchquery string<br />
--nmap                     perform a nmap scan in the hosts<br />
--setkey=SETKEY		       set your api key automatically<br />
-r RANGE, --range=RANGE    scan a range of ips. ex: 192.168.1.1-192.168.1.255<br />
-o OUTPUT, --output=OUTPUT specify a output file<br /><br />

Nmap Options:<br />
--sS                  TCP Syn Scan<br />
--sT                  TCP Connect Scan<br />
--sU                  UDP Scan

# Usage
<em>For One Host<em><br />
python shodanhat.py -i IP<br />
<em>For a list of Hosts</em><br />
python shodanhat.py -l list.txt<br />
You can also set a searchquery to make a specific query with '-s' option!

# ScreenShots
<img src="http://i.imgur.com/J4aAHov.jpg" /><br />
<img src="http://i.imgur.com/q3YTHm8.jpg" />