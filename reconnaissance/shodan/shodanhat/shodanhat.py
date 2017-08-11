#!/usr/bin/env python
# -*- coding: utf-8 -*-

import optparse, shodan, sys, nmap, urllib2, json, os
from constantes import *

class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'

def banner():
	print colors.GREEN + "███████╗██╗  ██╗ ██████╗ ██████╗  █████╗ ███╗   ██╗██╗  ██╗ █████╗ ████████╗"
	print "██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔══██╗████╗  ██║██║  ██║██╔══██╗╚══██╔══╝"
	print "███████╗███████║██║   ██║██║  ██║███████║██╔██╗ ██║███████║███████║   ██║   "
	print "╚════██║██╔══██║██║   ██║██║  ██║██╔══██║██║╚██╗██║██╔══██║██╔══██║   ██║   "
	print "███████║██║  ██║╚██████╔╝██████╔╝██║  ██║██║ ╚████║██║  ██║██║  ██║   ██║   "
	print "╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   "
	print ""
	print "Author: Everton a.k.a XGU4RD14N && Mateus a.k.a Dctor"
	print "Members HatBashBR: Johnny a.k.a UrdSys, Evelyn a.k.a Alyosha, Geovane"
	print "fb.com/hatbashbr"
	print "github.com/hatbashbr" + colors.END
	print colors.YELLOW + "[!] Legal Disclaimer: We aren't responsible for bad use of this tool!" + colors.END
	print ""
banner()

hosts = {}

def ipRange(start_ip, end_ip):
	start = list(map(int, start_ip.split(".")))
	end = list(map(int, end_ip.split(".")))
	temp = start
	ip_range = []

	ip_range.append(start_ip)
	while temp != end:
		start[3] += 1
		for i in (3, 2, 1):
			if temp[i] == 256:
				temp[i] = 0
				temp[i-1] += 1
		ip_range.append(".".join(map(str, temp)))

	return ip_range

def saveExploits(ip, port, o):
	if hosts[ip][port][0] == "" or hosts[ip][port][1] == "":
		o.write("    [-] No exploits could be found\n")
	else:
		query = "%s %s"%(hosts[ip][port][0], hosts[ip][port][1])
		query = query.replace(" ", "+")
		url = urllib2.urlopen("https://exploits.shodan.io/api/search?query=%s&key=%s"%(query, SHODAN_API_KEY))
		xpls = json.load(url)
		if xpls["total"] > 0:
			o.write("    Possible Exploits:\n")
			for i in xpls["matches"]:
				if i.has_key("cve"):
					for cve in i["cve"]:
						o.write("    [+] CVE: %s\n"%cve)
				elif i.has_key("_id"):
					o.write("    [+] ID: %s\n"%i["_id"])
		else:
			o.write("    [-] No exploits could be found\n")

def searchExploits(ip, port):
	if hosts[ip][port][0] == "" or hosts[ip][port][1] == "":
		print colors.FAIL + "    [-] No exploits could be found" + colors.END
	else:
		query = "%s %s"%(hosts[ip][port][0], hosts[ip][port][1])
		query = query.replace(" ", "+")
		url = urllib2.urlopen("https://exploits.shodan.io/api/search?query=%s&key=%s"%(query, SHODAN_API_KEY))
		xpls = json.load(url)
		if xpls["total"] > 0:
			print colors.GREEN +"    Possible Exploits:"
			for i in xpls["matches"]:
				if i.has_key("cve"):
					for cve in i["cve"]:
						print "    [+] CVE: %s"%cve
				elif i.has_key("_id"):
					print "    [+] ID: %s"%i["_id"]
			print colors.END,
		else:
			print colors.FAIL + "    [-] No exploits could be found" + colors.END

def saveInfo(host, o):
	o.write("IP: %s\n"%host["ip_str"])
	o.write("Organization: %s\n"%host.get("org", "n/a"))
	o.write("Operating System: %s\n"%host.get("os", "n/a"))
	o.write("Latitude: %s\n"%host["latitude"])
	o.write("Longitude: %s\n"%host["longitude"])
	o.write("City: %s\n"%host["city"])
	o.write("Hostnames:\n")
	if len(host["hostnames"]) == 0:
		o.write("  [-] No hostnames\n")
	else:
		for i in host["hostnames"]:
			o.write("  [+] %s\n"%str(i))
	if host.has_key('vulns'):
		o.write("Vulnerabilities:\n")
		for i in host["vulns"]:
			o.write("  [+] %s\n"%str(i))
			
	if options.nmap:
		hosts[str(host["ip_str"])] = {}
		ports = ""
		for item in host["data"]:
			if item == host["data"][-1]:
				ports += str(item["port"])
			else:
				ports += str(item["port"])+","
		args = options.scantype
		nm.scan(str(host["ip_str"]), ports, arguments=args)
		if str(host["ip_str"]) in nm.all_hosts():
			o.write("Ports:\n")
			for port in nm[str(host["ip_str"])]["tcp"]:
				hosts[host["ip_str"]][port] = [nm[host["ip_str"]]["tcp"][port]["product"],nm[host["ip_str"]]["tcp"][port]["version"]]
				o.write("  [+] %s\t%s %s %s\n"%(port, nm[host["ip_str"]]["tcp"][port]["product"], nm[host["ip_str"]]["tcp"][port]["version"], nm[host["ip_str"]]["tcp"][port]["extrainfo"]))
				saveExploits(host["ip_str"], port, o)
		else:
			o.write("Ports:\n")
			for item in host["data"]:
				print o.write("  [+] %s\n"%item["port"])
	else:
		o.write("Ports:\n")
		for item in host["data"]:
			o.write("  [+] %s\n"%item["port"])

def printInfo(host):
	print colors.GREEN + "IP: %s"%host["ip_str"]
	print "Organization: %s"%host.get("org", "n/a")
	print "Operating System: %s"%host.get("os", "n/a")
	print "Latitude: %s"%host["latitude"]
	print "Longitude: %s"%host["longitude"]
	print "City: %s"%host["city"]
	print "Hostnames:"
	if len(host["hostnames"]) == 0:
		print colors.FAIL + "  [-] No hostnames" + colors.END + colors.GREEN
	else:
		for i in host["hostnames"]:
			print "  [+] " + i
	if host.has_key('vulns'):
		print "Vulnerabilities:"
		for i in host["vulns"]:
			print "  [+] " +i
			
	if options.nmap:
		hosts[str(host["ip_str"])] = {}
		ports = ""
		for item in host["data"]:
			if item == host["data"][-1]:
				ports += str(item["port"])
			else:
				ports += str(item["port"])+","
		
		args = options.scantype
		nm.scan(str(host["ip_str"]), ports, arguments=args)
		if str(host["ip_str"]) in nm.all_hosts():
			print "Ports: "
			for port in nm[str(host["ip_str"])]["tcp"]:
				hosts[host["ip_str"]][port] = [nm[host["ip_str"]]["tcp"][port]["product"],nm[host["ip_str"]]["tcp"][port]["version"]]
				print colors.GREEN + "  [+] %s\t%s %s %s"%(port, nm[host["ip_str"]]["tcp"][port]["product"], nm[host["ip_str"]]["tcp"][port]["version"], nm[host["ip_str"]]["tcp"][port]["extrainfo"]) + colors.END
				searchExploits(host["ip_str"], port)
		else:
			print "Ports: "
			for item in host["data"]:
				print colors.GREEN + "  [+] %s"%item["port"] + colors.END
	else:
		print "Ports: "
		for item in host["data"]:
			print colors.GREEN + "  [+] %s"%item["port"] + colors.END
	print colors.END,
	
	

parser = optparse.OptionParser()
parser.add_option("-i", "--ip", dest="ip", help="info about one host", default="")
parser.add_option("-l", "--list", dest="list", help="info about a list of hosts", default="")
parser.add_option("-s", "--sq", dest="sq", help="searchquery string", default="")
parser.add_option("--nmap", dest="nmap", action="store_true", help="perform a nmap scan in the hosts")
parser.add_option("--setkey", dest="setkey", help="set your api key automatically", default="")
parser.add_option("-r", "--range", dest="range", help="scan a range of ips. ex: 192.168.1.1-192.168.1.255", default="")
parser.add_option("-o", "--output", dest="output", help="specify a output file", default="")
group = optparse.OptionGroup(parser, "Nmap Options")
group.add_option("--sS", dest="scantype", action="store_const", help="TCP Syn Scan", const="-sS")
group.add_option("--sT", dest="scantype", action="store_const", help="TCP Connect Scan", const="-sT")
group.add_option("--sU", dest="scantype", action="store_const", help="UDP Scan", const="-sU")
parser.add_option_group(group)
parser.set_defaults(scantype="-sT")
options, args = parser.parse_args()

if options.setkey != "":
	f = open("constantes.py", 'w')
	f.write('SHODAN_API_KEY = "%s"'%options.setkey)
	SHODAN_API_KEY = options.setkey

if SHODAN_API_KEY == "":
	print "You need to set the API Key in the file 'constantes.py' or with the '--setkey' option"
	sys.exit()
	
if options.ip != "" and options.list != "":
	print "You can't use '-i' with '-l'!"
	sys.exit()

api = shodan.Shodan(SHODAN_API_KEY)
nm = nmap.PortScanner()

if options.output != "":
	if os.path.isfile(options.output):
		try:
			ans = str(raw_input(colors.FAIL + "[-] File already exists, if you continue it will erase all the content of the file. continue? (y/N): " + colors.END))
			if ans != "y" and ans != "Y":
				print colors.GREEN + "[+] Exiting..." + colors.END
				sys.exit()
		except SyntaxError:
			print colors.GREEN + "[+] Exiting..." + colors.END
			sys.exit()
	o = open(options.output, 'w')

if options.ip != "":
	if options.output != "":
		try:
			print colors.GREEN + "[+] Writing host's info to the file" + colors.END
			host = api.host(options.ip)
			saveInfo(host, o)
		except Exception as e:
			o.write("[-] "+ str(ip) +"\n  Error: "+str(e)+"\n\n")
	else:
		try:
			host = api.host(options.ip)
			printInfo(host)
		except Exception as e:
			print colors.FAIL + "[-] "+ str(options.ip) +"\n  Error: "+str(e) + colors.END
			print
elif options.list != "":
	f = open(options.list)
	if options.output != "":
		print colors.GREEN + "[+] Writing hosts' info to the file" + colors.END
		for ip in f.readlines():
			try:
				host = api.host(ip)
				saveInfo(host, o)
				o.write('\n')
			except Exception as e:
				o.write("[-] "+ str(ip) +"\n  Error: "+str(e)+"\n\n")
	else:
		for ip in f.readlines():
			try:
				host = api.host(ip)
				printInfo(host)
				print
			except Exception as e:
				print colors.FAIL + "[-] "+ str(options.ip) +"\n  Error: "+str(e) + colors.END
				print
elif options.range != "":
	first = options.range.split('-')[0]
	second = options.range.split('-')[1]
	
	#Verify if is a valid range
	if len(first.split('.')) != 4 or len(second.split('.')) != 4:
		print "[-] Invalid range! see the help to use the --range option."
		sys.exit()
	
	#Verify if is a valid IP
	for i in first.split('.'):
		if int(i) > 255:
			print "[-] Invalid IP! see the help to use the --range option."
			sys.exit()
			
	for i in second.split('.'):
		if int(i) > 255:
			print "[-] Invalid IP! see the help to use the --range option."
			sys.exit()
			
	firstSplited = first.split('.')
	secondSplited = second.split('.')
	firstSum = int(firstSplited[0])+int(firstSplited[1])+int(firstSplited[2])+int(firstSplited[3])
	secondSum = int(secondSplited[0])+int(secondSplited[1])+int(secondSplited[2])+int(secondSplited[3])
	
	if(firstSum >= secondSum):
		print "[-] Invalid range! see the help to use the --range option."
		sys.exit()
	
	iprange = ipRange(first, second)
	
	if options.output != "":
		print colors.GREEN + "[+] Writing hosts' info to the file" + colors.END
		for ip in iprange:
			try:
				host = api.host(ip)
				saveInfo(host, o)
				o.write('\n')
			except Exception as e:
				o.write("[-] "+ str(ip) +"\n  Error: "+str(e)+"\n\n")
	else:
		for ip in iprange:
			try:
				host = api.host(ip)
				printInfo(host)
				print
			except Exception as e:
				print colors.FAIL + "[-] "+ str(ip) +"\n  Error: "+str(e) + colors.END
				print
if options.sq != "":
	try:
		result = api.search(options.sq)
		if options.output != "":
			print colors.GREEN + "[+] Writing query results to the file" + colors.END
			o.write("##### IP's that match the query '%s' #####\n"%options.sq)
		else:
			print "##### IP's that match the query '%s' #####"%options.sq
		for service in result['matches']:
			if options.output != "":
				o.write(service['ip_str']+"\n")
			else:
				print service['ip_str']
	except Exception as e:
		print "Error: "+str(e)
